from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now

from .models import Notification, NotificationPreference, ReportSchedule
from .models import Webhook
import hashlib
import hmac
import json
import requests
from django.utils.timezone import now


def advance_report_schedule(schedule, executed_at=None):
    executed_at = executed_at or now()
    schedule.last_run_at = executed_at
    schedule.next_run_at = _next_run_at(schedule.frequency, executed_at)
    schedule.save(update_fields=['last_run_at', 'next_run_at', 'updated_at'])

    Notification.objects.create(
        user=schedule.created_by,
        panel=schedule.panel,
        type=Notification.Type.SYSTEM,
        message=f'Scheduled {schedule.report_type} report was processed as {schedule.export_format.upper()}.',
    )
    return schedule


def _next_run_at(frequency, current=None):
    current = current or now()

    if frequency == ReportSchedule.Frequency.DAILY:
        return current + timedelta(days=1)
    if frequency == ReportSchedule.Frequency.WEEKLY:
        return current + timedelta(days=7)
    return current + timedelta(days=30)


@shared_task(name='expenses.tasks.send_webhook_event')
def send_webhook_event(webhook_id, payload):
    """Send a single webhook delivery with HMAC-SHA256 signature if secret present."""
    try:
        webhook = Webhook.objects.get(id=webhook_id, is_active=True)
    except Webhook.DoesNotExist:
        return {
            "webhook_id": str(webhook_id),
            "status": "skipped",
            "reason": "webhook not found or inactive",
        }

    headers = {"Content-Type": "application/json"}
    body = json.dumps(payload)

    # Sign payload if secret configured
    if webhook.secret:
        signature = hmac.new(webhook.secret.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).hexdigest()
        headers["X-Webhook-Signature"] = signature

    try:
        resp = requests.post(webhook.url, data=body, headers=headers, timeout=10)
        webhook.last_attempt_at = now()
        if resp.status_code >= 200 and resp.status_code < 300:
            webhook.failure_count = 0
            webhook.save(update_fields=["last_attempt_at", "failure_count"])
            return {"webhook_id": str(webhook.id), "status": "delivered", "status_code": resp.status_code}
        else:
            webhook.failure_count = webhook.failure_count + 1
            webhook.save(update_fields=["last_attempt_at", "failure_count"])
            return {"webhook_id": str(webhook.id), "status": "failed", "status_code": resp.status_code}
    except Exception as exc:
        webhook.failure_count = webhook.failure_count + 1
        webhook.last_attempt_at = now()
        webhook.save(update_fields=["last_attempt_at", "failure_count"])
        return {"webhook_id": str(webhook.id), "status": "error", "reason": str(exc)}


@shared_task(name='expenses.tasks.notify_webhooks')
def notify_webhooks(panel_id, event, payload):
    """Find active webhooks for a panel subscribed to `event` and enqueue deliveries."""
    webhooks = Webhook.objects.filter(panel_id=panel_id, is_active=True, events__contains=[event])
    results = []
    for wh in webhooks:
        results.append(send_webhook_event.delay(str(wh.id), payload))
    return {"queued": len(results)}


@shared_task(name='expenses.tasks.process_due_report_schedules')
def process_due_report_schedules():
    due_schedules = (
        ReportSchedule.objects.select_related('panel', 'created_by')
        .filter(is_active=True, next_run_at__lte=now())
        .order_by('next_run_at')
    )

    processed = 0
    for schedule in due_schedules:
        advance_report_schedule(schedule)
        # notify webhooks that a scheduled report ran
        try:
            payload = {
                "event": "report.run",
                "schedule_id": str(schedule.id),
                "panel_id": str(schedule.panel.id),
                "report_type": schedule.report_type,
                "export_format": schedule.export_format,
                "executed_at": now().isoformat(),
            }
            notify_webhooks.delay(str(schedule.panel.id), "report.run", payload)
        except Exception:
            pass
        if NotificationPreference.objects.filter(
            user=schedule.created_by,
            panel=schedule.panel,
            enabled=True,
            delivery=NotificationPreference.Delivery.EMAIL,
        ).exists():
            send_mail(
                subject=f'Scheduled {schedule.report_type} report ready',
                message=(
                    f'Your {schedule.report_type} report for panel "{schedule.panel.name}" '
                    f'was generated in {schedule.export_format.upper()} format.'
                ),
                from_email=None,
                recipient_list=[schedule.created_by.email],
            )

        processed += 1

    return processed


@shared_task(name='expenses.tasks.send_notification_email')
def send_notification_email(notification_id):
    notification = Notification.objects.select_related('user', 'panel').get(id=notification_id)
    send_mail(
        subject=f'Expense Manager: {notification.type.replace("_", " ").title()}',
        message=notification.message,
        from_email=None,
        recipient_list=[notification.user.email],
    )
    return str(notification.id)


@shared_task(name='expenses.tasks.process_due_recurring_expenses')
def process_due_recurring_expenses():
    """Process due recurring expenses and create actual expenses."""
    from .models import RecurringExpense, Expense
    from datetime import date

    today = date.today()
    recurring = (
        RecurringExpense.objects.select_related('panel', 'category', 'created_by')
        .filter(is_active=True, start_date__lte=today)
    )

    processed = 0
    for rec in recurring:
        if rec.end_date and today > rec.end_date:
            continue

        last_created = rec.last_created_at or rec.start_date - timedelta(days=1)
        next_due = _next_recurring_date(rec.frequency, last_created)

        if next_due <= today:
            expense = Expense.objects.create(
                panel=rec.panel,
                category=rec.category,
                created_by=rec.created_by,
                amount=rec.amount,
                date=today,
                description=f"{rec.description} (recurring)" if rec.description else "Recurring expense",
            )

            rec.last_created_at = today
            rec.save(update_fields=['last_created_at', 'updated_at'])

            # Trigger webhook notification
            try:
                payload = {
                    "event": "expense.created",
                    "expense_id": str(expense.id),
                    "panel_id": str(rec.panel.id),
                    "amount": str(expense.amount),
                    "date": expense.date.isoformat(),
                    "created_by": str(expense.created_by.id),
                    "is_recurring": True,
                }
                notify_webhooks.delay(str(rec.panel.id), "expense.created", payload)
            except Exception:
                pass

            processed += 1

    return processed


def _next_recurring_date(frequency, last_created):
    """Calculate next due date for recurring expense."""
    from .models import RecurringExpense

    if frequency == RecurringExpense.Frequency.DAILY:
        return last_created + timedelta(days=1)
    if frequency == RecurringExpense.Frequency.WEEKLY:
        return last_created + timedelta(days=7)
    if frequency == RecurringExpense.Frequency.BIWEEKLY:
        return last_created + timedelta(days=14)
    if frequency == RecurringExpense.Frequency.MONTHLY:
        # add 30 days as approximation
        return last_created + timedelta(days=30)
    if frequency == RecurringExpense.Frequency.QUARTERLY:
        return last_created + timedelta(days=90)
    if frequency == RecurringExpense.Frequency.ANNUAL:
        return last_created + timedelta(days=365)
    return last_created