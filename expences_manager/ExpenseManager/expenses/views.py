import csv
from datetime import timedelta
from decimal import Decimal
from io import BytesIO, StringIO

from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Count, Max, Min, Sum
from django.db.models.functions import TruncMonth
from django.urls import reverse
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView

from .models import AuditLog, Budget, Category, Expense, Notification, Panel, PanelUser, ReportSchedule, User
from .models import Invitation, NotificationPreference
from .audit import log_audit_event
from .permissions import IsPanelMember, IsPanelMemberReadOnly, IsPanelOwner, IsPanelOwnerOrEditor, ViewerReadOnly
from .serializers import (
    BudgetSerializer,
    CategorySerializer,
    ExpenseSerializer,
    NotificationSerializer,
    PanelSerializer,
    PanelUserSerializer,
    UserSerializer,
    NotificationPreferenceSerializer,
    AuditLogSerializer,
    ReportScheduleSerializer,
    InvitationSerializer,
)
from .tasks import advance_report_schedule, send_notification_email, notify_webhooks


def _export_rows_as_csv(filename, headers, rows):
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(headers)
    writer.writerows(rows)
    response = HttpResponse(buffer.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
    return response


def _export_rows_as_xlsx(filename, headers, rows):
    from openpyxl import Workbook

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Report"
    worksheet.append(headers)
    for row in rows:
        worksheet.append(row)

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}.xlsx"'
    return response


def _export_rows_as_pdf(filename, title, headers, rows):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    output = BytesIO()
    pdf = canvas.Canvas(output, pagesize=letter)
    width, height = letter

    y = height - 40
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, title)
    y -= 24

    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(40, y, " | ".join(str(h) for h in headers))
    y -= 16
    pdf.setFont("Helvetica", 9)

    for row in rows:
        line = " | ".join(str(value) for value in row)
        if y < 40:
            pdf.showPage()
            y = height - 40
            pdf.setFont("Helvetica", 9)
        pdf.drawString(40, y, line[:140])
        y -= 14

    pdf.save()
    output.seek(0)

    response = HttpResponse(output.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'
    return response


def _build_export_response(filename, title, headers, rows, export_format):
    if export_format == "csv":
        return _export_rows_as_csv(filename, headers, rows)
    if export_format == "xlsx":
        return _export_rows_as_xlsx(filename, headers, rows)
    if export_format == "pdf":
        return _export_rows_as_pdf(filename, title, headers, rows)
    return None


class UserRegistrationView(APIView):
    """Register a new user."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            log_audit_event(
                actor=user,
                action=AuditLog.Action.CREATE,
                instance=user,
                description="User registered",
                request=request,
            )
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Include user and panel claims in JWT tokens."""

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        request = self.context.get("request")
        panel = None
        role = None

        if request:
            panel_id = request.data.get("panel_id")
            if panel_id:
                try:
                    panel = Panel.objects.get(id=panel_id)
                    if panel.owner != user:
                        membership = PanelUser.objects.get(user=user, panel=panel)
                        role = membership.role
                    else:
                        role = PanelUser.Role.OWNER
                except (Panel.DoesNotExist, PanelUser.DoesNotExist):
                    panel = None

        if panel is None:
            panel = Panel.objects.filter(owner=user).first()
            if panel is None:
                membership = PanelUser.objects.filter(user=user).select_related("panel").first()
                if membership:
                    panel = membership.panel
                    role = membership.role
            else:
                role = PanelUser.Role.OWNER

        refresh = self.get_token(user)
        refresh["user_id"] = str(user.id)
        refresh["panel_id"] = str(panel.id) if panel else None
        refresh["role"] = role
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user_id"] = str(user.id)
        data["panel_id"] = str(panel.id) if panel else None
        data["role"] = role
        return data


class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        log_audit_event(
            actor=user,
            action=AuditLog.Action.LOGIN,
            entity_type="user",
            entity_id=str(user.id),
            description="User logged in",
            request=request,
        )
        return Response(serializer.validated_data)


class TokenRefreshViewCustom(TokenRefreshView):
    """Refresh JWT access token."""

    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """User profile management."""

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=["get"])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["put", "patch"])
    def update_profile(self, request):
        """Update current user profile (excluding password)."""
        user = request.user
        if "password" in request.data:
            return Response(
                {"detail": "Use change password endpoint"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportSummaryView(APIView):
    """Panel-scoped expense and budget summary report."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        panel_id = request.query_params.get("panel_id")
        export_format = request.query_params.get("export", "json").lower()
        if not panel_id:
            return Response(
                {"detail": "panel_id query param required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        date_from = parse_date(request.query_params.get("date_from") or "")
        date_to = parse_date(request.query_params.get("date_to") or "")
        if request.query_params.get("date_from") and not date_from:
            return Response(
                {"detail": "date_from must be YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.query_params.get("date_to") and not date_to:
            return Response(
                {"detail": "date_to must be YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if date_from and date_to and date_from > date_to:
            return Response(
                {"detail": "date_from cannot be after date_to"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            panel = Panel.objects.get(id=panel_id)
        except Panel.DoesNotExist:
            return Response(
                {"detail": "Panel not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not self._user_has_panel_access(request.user, panel):
            return Response(
                {"detail": "Access denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        cache_key = self._build_cache_key(request.user.id, panel_id, date_from, date_to, export_format)
        cached_payload = cache.get(cache_key)
        if cached_payload is not None:
            return self._render_report(cached_payload, export_format)

        expenses = Expense.objects.filter(panel=panel, deleted_at__isnull=True)
        if date_from:
            expenses = expenses.filter(date__gte=date_from)
        if date_to:
            expenses = expenses.filter(date__lte=date_to)

        totals = expenses.aggregate(
            expense_count=Count("id"),
            total_spent=Sum("amount"),
            first_expense_date=Min("date"),
            last_expense_date=Max("date"),
        )

        category_breakdown = [
            {
                "category_id": row["category_id"],
                "category_name": row["category__name"],
                "expense_count": row["expense_count"],
                "total_spent": row["total_spent"],
            }
            for row in expenses.values("category_id", "category__name").annotate(
                expense_count=Count("id"),
                total_spent=Sum("amount"),
            ).order_by("-total_spent", "category__name")
        ]

        budget_snapshot = []
        for budget in Budget.objects.filter(panel=panel):
            budget_expenses = Expense.objects.filter(panel=panel, deleted_at__isnull=True)
            if budget.category_id:
                budget_expenses = budget_expenses.filter(category=budget.category)
            if budget.start_date:
                budget_expenses = budget_expenses.filter(date__gte=budget.start_date)
            if budget.end_date:
                budget_expenses = budget_expenses.filter(date__lte=budget.end_date)
            if date_from:
                budget_expenses = budget_expenses.filter(date__gte=date_from)
            if date_to:
                budget_expenses = budget_expenses.filter(date__lte=date_to)

            spent = budget_expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0")
            status_info = "on_track"
            if spent >= budget.limit_amount:
                status_info = "exceeded"
            elif (spent * Decimal("100") / budget.limit_amount) >= budget.alert_threshold:
                status_info = "warning"

            budget_snapshot.append(
                {
                    "budget_id": budget.id,
                    "limit": budget.limit_amount,
                    "spent": spent,
                    "status": status_info,
                }
            )

        report_payload = {
            "panel": {
                "id": panel.id,
                "name": panel.name,
            },
            "date_range": {
                "from": date_from,
                "to": date_to,
            },
            "expenses": {
                "count": totals["expense_count"],
                "total_spent": totals["total_spent"] or Decimal("0"),
                "first_expense_date": totals["first_expense_date"],
                "last_expense_date": totals["last_expense_date"],
                "by_category": category_breakdown,
            },
            "budgets": budget_snapshot,
        }

        cache.set(cache_key, report_payload, 300)
        return self._render_report(report_payload, export_format)

    def _render_report(self, payload, export_format):
        if export_format in {"csv", "pdf", "xlsx"}:
            return self._render_export(payload, export_format)
        return Response(payload)

    def _render_export(self, payload, export_format):
        rows = [
            ["panel", "id", payload["panel"]["id"]],
            ["panel", "name", payload["panel"]["name"]],
            ["expenses", "count", payload["expenses"]["count"]],
            ["expenses", "total_spent", payload["expenses"]["total_spent"]],
            ["expenses", "first_expense_date", payload["expenses"]["first_expense_date"]],
            ["expenses", "last_expense_date", payload["expenses"]["last_expense_date"]],
        ]

        for row in payload["expenses"]["by_category"]:
            rows.append(["category", row["category_name"], row["total_spent"]])
        for row in payload["budgets"]:
            rows.append(["budget", row["budget_id"], row["status"]])

        return _build_export_response(
            filename="report-summary",
            title="Summary Report",
            headers=["section", "name", "value"],
            rows=rows,
            export_format=export_format,
        )

    def _build_cache_key(self, user_id, panel_id, date_from, date_to, export_format):
        return f"report-summary:{user_id}:{panel_id}:{date_from or ''}:{date_to or ''}:{export_format}"

    def _user_has_panel_access(self, user, panel):
        if panel.owner == user:
            return True
        return PanelUser.objects.filter(user=user, panel=panel).exists()


class ReportMonthlyView(APIView):
    """Panel-scoped monthly expense totals."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        panel_id = request.query_params.get("panel_id")
        export_format = request.query_params.get("export", "json").lower()
        if not panel_id:
            return Response(
                {"detail": "panel_id query param required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        date_from = parse_date(request.query_params.get("date_from") or "")
        date_to = parse_date(request.query_params.get("date_to") or "")
        if request.query_params.get("date_from") and not date_from:
            return Response(
                {"detail": "date_from must be YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.query_params.get("date_to") and not date_to:
            return Response(
                {"detail": "date_to must be YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if date_from and date_to and date_from > date_to:
            return Response(
                {"detail": "date_from cannot be after date_to"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            panel = Panel.objects.get(id=panel_id)
        except Panel.DoesNotExist:
            return Response(
                {"detail": "Panel not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not self._user_has_panel_access(request.user, panel):
            return Response(
                {"detail": "Access denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        cache_key = f"report-monthly:{request.user.id}:{panel_id}:{date_from or ''}:{date_to or ''}:{export_format}"
        cached_payload = cache.get(cache_key)
        if cached_payload is not None:
            return self._render_report(cached_payload, export_format)

        expenses = Expense.objects.filter(panel=panel, deleted_at__isnull=True)
        if date_from:
            expenses = expenses.filter(date__gte=date_from)
        if date_to:
            expenses = expenses.filter(date__lte=date_to)

        monthly_rows = expenses.annotate(month=TruncMonth("date")).values("month").annotate(
            expense_count=Count("id"),
            total_spent=Sum("amount"),
        ).order_by("month")

        monthly = [
            {
                "month": row["month"].strftime("%Y-%m") if row["month"] else None,
                "expense_count": row["expense_count"],
                "total_spent": row["total_spent"] or Decimal("0"),
            }
            for row in monthly_rows
        ]

        report_payload = {
            "panel": {
                "id": panel.id,
                "name": panel.name,
            },
            "date_range": {
                "from": date_from,
                "to": date_to,
            },
            "monthly": monthly,
        }

        cache.set(cache_key, report_payload, 300)
        return self._render_report(report_payload, export_format)

    def _render_report(self, payload, export_format):
        if export_format in {"csv", "pdf", "xlsx"}:
            rows = [[row["month"], row["expense_count"], row["total_spent"]] for row in payload["monthly"]]
            return _build_export_response(
                filename="report-monthly",
                title="Monthly Report",
                headers=["month", "expense_count", "total_spent"],
                rows=rows,
                export_format=export_format,
            )
        return Response(payload)

    def _user_has_panel_access(self, user, panel):
        if panel.owner == user:
            return True
        return PanelUser.objects.filter(user=user, panel=panel).exists()


class ReportTrendsView(APIView):
    """Panel-scoped category trend report by month."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        panel_id = request.query_params.get("panel_id")
        category_id = request.query_params.get("category_id")
        export_format = request.query_params.get("export", "json").lower()
        if not panel_id:
            return Response(
                {"detail": "panel_id query param required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        date_from = parse_date(request.query_params.get("date_from") or "")
        date_to = parse_date(request.query_params.get("date_to") or "")
        if request.query_params.get("date_from") and not date_from:
            return Response(
                {"detail": "date_from must be YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.query_params.get("date_to") and not date_to:
            return Response(
                {"detail": "date_to must be YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if date_from and date_to and date_from > date_to:
            return Response(
                {"detail": "date_from cannot be after date_to"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            panel = Panel.objects.get(id=panel_id)
        except Panel.DoesNotExist:
            return Response(
                {"detail": "Panel not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not self._user_has_panel_access(request.user, panel):
            return Response(
                {"detail": "Access denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        cache_key = (
            f"report-trends:{request.user.id}:{panel_id}:{category_id or ''}:"
            f"{date_from or ''}:{date_to or ''}:{export_format}"
        )
        cached_payload = cache.get(cache_key)
        if cached_payload is not None:
            return self._render_report(cached_payload, export_format)

        expenses = Expense.objects.filter(panel=panel, deleted_at__isnull=True)
        if category_id:
            expenses = expenses.filter(category_id=category_id)
        if date_from:
            expenses = expenses.filter(date__gte=date_from)
        if date_to:
            expenses = expenses.filter(date__lte=date_to)

        trend_rows = expenses.annotate(month=TruncMonth("date")).values(
            "month",
            "category_id",
            "category__name",
        ).annotate(
            expense_count=Count("id"),
            total_spent=Sum("amount"),
        ).order_by("month", "category__name")

        month_totals = {}
        for row in trend_rows:
            month_key = row["month"]
            month_totals[month_key] = month_totals.get(month_key, Decimal("0")) + (row["total_spent"] or Decimal("0"))

        trends = []
        for row in trend_rows:
            month_key = row["month"]
            month_total = month_totals.get(month_key, Decimal("0"))
            total_spent = row["total_spent"] or Decimal("0")
            share_pct = Decimal("0")
            if month_total > 0:
                share_pct = (total_spent * Decimal("100")) / month_total

            trends.append(
                {
                    "month": month_key.strftime("%Y-%m") if month_key else None,
                    "category_id": row["category_id"],
                    "category_name": row["category__name"],
                    "expense_count": row["expense_count"],
                    "total_spent": total_spent,
                    "share_of_month_pct": round(share_pct, 2),
                }
            )

        report_payload = {
            "panel": {
                "id": panel.id,
                "name": panel.name,
            },
            "date_range": {
                "from": date_from,
                "to": date_to,
            },
            "category_id": category_id,
            "trends": trends,
        }

        cache.set(cache_key, report_payload, 300)
        return self._render_report(report_payload, export_format)

    def _render_report(self, payload, export_format):
        if export_format in {"csv", "pdf", "xlsx"}:
            rows = [
                [
                    row["month"],
                    row["category_name"],
                    row["expense_count"],
                    row["total_spent"],
                    row["share_of_month_pct"],
                ]
                for row in payload["trends"]
            ]
            return _build_export_response(
                filename="report-trends",
                title="Trends Report",
                headers=["month", "category_name", "expense_count", "total_spent", "share_of_month_pct"],
                rows=rows,
                export_format=export_format,
            )
        return Response(payload)

    def _user_has_panel_access(self, user, panel):
        if panel.owner == user:
            return True
        return PanelUser.objects.filter(user=user, panel=panel).exists()


class PanelViewSet(viewsets.ModelViewSet):
    """Panel (workspace/tenant) management."""

    serializer_class = PanelSerializer
    permission_classes = [IsAuthenticated, IsPanelMember]
    lookup_field = "id"

    def get_queryset(self):
        """Return panels where user is a member."""
        user_panels = PanelUser.objects.filter(user=self.request.user).values_list("panel_id", flat=True)
        user_owned_panels = Panel.objects.filter(owner=self.request.user).values_list("id", flat=True)
        all_panel_ids = set(list(user_panels) + list(user_owned_panels))
        return Panel.objects.filter(id__in=all_panel_ids).order_by('-created_at')

    def perform_create(self, serializer):
        """Set owner to current user."""
        serializer.save(owner=self.request.user)
        panel = serializer.instance
        PanelUser.objects.create(user=self.request.user, panel=panel, role=PanelUser.Role.OWNER, joined_at=now())
        log_audit_event(
            actor=self.request.user,
            panel=panel,
            action=AuditLog.Action.CREATE,
            instance=panel,
            description="Panel created",
            request=self.request,
        )

    def perform_update(self, serializer):
        """Only owner can update."""
        if serializer.instance.owner != self.request.user:
            raise serializers.ValidationError("Only panel owner can update.")
        serializer.save()
        log_audit_event(
            actor=self.request.user,
            panel=serializer.instance,
            action=AuditLog.Action.UPDATE,
            instance=serializer.instance,
            description="Panel updated",
            request=self.request,
        )

    def perform_destroy(self, instance):
        """Only owner can delete."""
        if instance.owner != self.request.user:
            raise serializers.ValidationError("Only panel owner can delete.")
        log_audit_event(
            actor=self.request.user,
            panel=instance,
            action=AuditLog.Action.DELETE,
            instance=instance,
            description="Panel deleted",
            request=self.request,
        )
        instance.delete()

    @action(detail=True, methods=["get"])
    def members(self, request, id=None):
        """List all members in a panel."""
        panel = self.get_object()
        members = PanelUser.objects.filter(panel=panel)
        serializer = PanelUserSerializer(members, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def invite_user(self, request, id=None):
        """Invite a user to the panel."""
        panel = self.get_object()
        if panel.owner != request.user:
            return Response(
                {"detail": "Only panel owner can invite"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Support two modes: direct (user_id) or email invitation (email)
        user_id = request.data.get("user_id")
        email = request.data.get("email")
        role = request.data.get("role", PanelUser.Role.VIEWER)

        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            membership, created = PanelUser.objects.get_or_create(
                user=user,
                panel=panel,
                defaults={"role": role, "invited_by": request.user, "joined_at": now()},
            )

            if not created:
                membership.role = role
                membership.save()

            self._send_invitation_email(panel, user.email, role, inviter=request.user, token=None)
            log_audit_event(
                actor=request.user,
                panel=panel,
                action=AuditLog.Action.INVITE,
                instance=membership,
                description=f"Direct invite for {user.email}",
                metadata={"mode": "direct", "role": role},
                request=request,
            )

            return Response(PanelUserSerializer(membership).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        if email:
            # Create an invitation token and record the invitation.
            import secrets

            token = secrets.token_urlsafe(32)
            invitation = Invitation.objects.create(
                panel=panel, email=email, token=token, role=role, invited_by=request.user
            )

            # Create an in-app notification for the inviter (and optionally for the email owner later)
            Notification.objects.create(
                user=request.user,
                panel=panel,
                type=Notification.Type.PANEL_INVITATION,
                message=f"Invitation sent to {email} for panel {panel.name}",
            )

            self._send_invitation_email(panel, email, role, inviter=request.user, token=token)
            log_audit_event(
                actor=request.user,
                panel=panel,
                action=AuditLog.Action.INVITE,
                instance=invitation,
                description=f"Email invite sent to {email}",
                metadata={"mode": "email", "role": role, "token": token},
                request=request,
            )

            return Response(InvitationSerializer(invitation).data, status=status.HTTP_201_CREATED)

        return Response({"detail": "user_id or email is required"}, status=status.HTTP_400_BAD_REQUEST)

    def _send_invitation_email(self, panel, recipient_email, role, inviter, token):
        accept_path = reverse("invitation-accept")
        invite_details = [
            f"You have been invited to join the panel '{panel.name}' as {role}.",
            f"Invited by: {inviter.username} ({inviter.email})",
        ]
        if token:
            invite_details.append(f"Invitation token: {token}")
            invite_details.append(f"Accept endpoint: {accept_path}")
            invite_details.append("Use the token with the accept endpoint after logging in with this email address.")
        else:
            invite_details.append("You were added directly to the panel and can log in to access it immediately.")

        send_mail(
            subject=f"Expense Manager invitation to {panel.name}",
            message="\n".join(invite_details),
            from_email=None,
            recipient_list=[recipient_email],
            fail_silently=False,
        )


class PanelUserViewSet(viewsets.ModelViewSet):
    """Panel membership management."""

    serializer_class = PanelUserSerializer
    permission_classes = [IsAuthenticated, IsPanelMember]
    lookup_field = "id"

    def get_queryset(self):
        """Return memberships for user's panels."""
        user_panel_ids = PanelUser.objects.filter(user=self.request.user).values_list("panel_id", flat=True)
        return PanelUser.objects.filter(panel_id__in=user_panel_ids)

    def perform_update(self, serializer):
        """Only panel owner can update memberships."""
        if serializer.instance.panel.owner != self.request.user:
            raise serializers.ValidationError("Only panel owner can update memberships.")
        serializer.save()

    def perform_destroy(self, instance):
        """Only panel owner can remove memberships."""
        if instance.panel.owner != self.request.user:
            raise serializers.ValidationError("Only panel owner can remove memberships.")
        instance.delete()

    @action(detail=True, methods=["patch"])
    def change_role(self, request, id=None):
        """Change a member's role (owner only)."""
        membership = self.get_object()
        if membership.panel.owner != request.user:
            return Response(
                {"detail": "Only panel owner can change roles"},
                status=status.HTTP_403_FORBIDDEN,
            )

        new_role = request.data.get("role")
        if new_role not in [choice[0] for choice in PanelUser.Role.choices]:
            return Response(
                {"detail": "Invalid role"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership.role = new_role
        membership.save()
        log_audit_event(
            actor=request.user,
            panel=membership.panel,
            action=AuditLog.Action.CHANGE_ROLE,
            instance=membership,
            description=f"Changed role to {new_role}",
            request=request,
        )
        return Response(PanelUserSerializer(membership).data)

    @action(detail=True, methods=["delete"])
    def remove_member(self, request, id=None):
        """Remove a member from panel (owner only)."""
        membership = self.get_object()
        if membership.panel.owner != request.user:
            return Response(
                {"detail": "Only panel owner can remove members"},
                status=status.HTTP_403_FORBIDDEN,
            )

        membership.delete()
        log_audit_event(
            actor=request.user,
            panel=membership.panel,
            action=AuditLog.Action.DELETE,
            instance=membership,
            description="Removed panel member",
            request=request,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class InvitationAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"detail": "token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invitation = Invitation.objects.get(token=token)
        except Invitation.DoesNotExist:
            return Response({"detail": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the authenticated user's email matches the invitation, or allow admin-like acceptance
        if request.user.email.lower() != invitation.email.lower():
            return Response({"detail": "Invitation email does not match user email"}, status=status.HTTP_403_FORBIDDEN)

        # Create membership
        membership, created = PanelUser.objects.get_or_create(
            user=request.user,
            panel=invitation.panel,
            defaults={"role": invitation.role, "invited_by": invitation.invited_by, "joined_at": now()},
        )

        invitation.accepted_at = now()
        invitation.accepted_by = request.user
        invitation.save()
        log_audit_event(
            actor=request.user,
            panel=invitation.panel,
            action=AuditLog.Action.ACCEPT,
            instance=invitation,
            description="Accepted invitation",
            request=request,
        )

        Notification.objects.create(
            user=request.user,
            panel=invitation.panel,
            type=Notification.Type.PANEL_INVITATION,
            message=f"You joined panel {invitation.panel.name} as {membership.role}",
        )

        return Response(PanelUserSerializer(membership).data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            log_audit_event(
                actor=request.user,
                action=AuditLog.Action.LOGOUT,
                entity_type="user",
                entity_id=str(request.user.id),
                description="User logged out",
                request=request,
            )
            return Response({"detail": "Logged out"})
        except Exception:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "email required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response({"detail": "If the email exists, a reset link will be sent."})

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(str(user.id)))
        reset_link = f"/api/auth/password_reset_confirm/?uid={uid}&token={token}"

        # Send email (console backend in dev)
        send_mail(
            subject="Password reset for Expense Manager",
            message=f"Use this link to reset your password: {reset_link}",
            from_email=None,
            recipient_list=[user.email],
        )
        log_audit_event(
            actor=user,
            action=AuditLog.Action.PASSWORD_RESET,
            entity_type="user",
            entity_id=str(user.id),
            description="Password reset requested",
            metadata={"email": user.email},
            request=request,
        )

        return Response({"detail": "If the email exists, a reset link will be sent."})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        if not uid or not token or not new_password:
            return Response({"detail": "uid, token and new_password are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=uid_decoded)
        except Exception:
            return Response({"detail": "Invalid uid"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        log_audit_event(
            actor=user,
            action=AuditLog.Action.PASSWORD_RESET,
            entity_type="user",
            entity_id=str(user.id),
            description="Password reset completed",
            request=request,
        )
        return Response({"detail": "Password has been reset"})


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """Manage notification preferences for users within panels."""

    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        # Return preferences for the current user across their panels
        user_panel_ids = PanelUser.objects.filter(user=self.request.user).values_list("panel_id", flat=True)
        user_owned_panel_ids = Panel.objects.filter(owner=self.request.user).values_list("id", flat=True)
        all_panel_ids = list(user_panel_ids) + list(user_owned_panel_ids)
        return NotificationPreference.objects.filter(user=self.request.user, panel_id__in=all_panel_ids).order_by(
            "panel_id",
            "user_id",
            "type",
        )

    def perform_create(self, serializer):
        # Ensure the preference belongs to the requesting user
        serializer.save(user=self.request.user)


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only audit trail for accessible panels."""

    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        user_panel_ids = PanelUser.objects.filter(user=self.request.user).values_list("panel_id", flat=True)
        owned_panel_ids = Panel.objects.filter(owner=self.request.user).values_list("id", flat=True)
        panel_ids = list(user_panel_ids) + list(owned_panel_ids)
        queryset = AuditLog.objects.filter(panel_id__in=panel_ids)
        panel_id = self.request.query_params.get("panel_id")
        if panel_id:
            queryset = queryset.filter(panel_id=panel_id)
        return queryset.order_by("-created_at")


class ReportScheduleViewSet(viewsets.ModelViewSet):
    """Manage recurring report export schedules."""

    serializer_class = ReportScheduleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        user_panel_ids = PanelUser.objects.filter(user=self.request.user).values_list("panel_id", flat=True)
        owned_panel_ids = Panel.objects.filter(owner=self.request.user).values_list("id", flat=True)
        panel_ids = list(user_panel_ids) + list(owned_panel_ids)
        return ReportSchedule.objects.filter(panel_id__in=panel_ids).order_by("-created_at")

    def perform_create(self, serializer):
        panel = serializer.validated_data.get("panel")
        if not self._user_has_panel_access(panel):
            raise serializers.ValidationError("User cannot create schedules for this panel")
        schedule = serializer.save(created_by=self.request.user)
        log_audit_event(
            actor=self.request.user,
            panel=panel,
            action=AuditLog.Action.CREATE,
            instance=schedule,
            description="Report schedule created",
            request=self.request,
        )

    def perform_update(self, serializer):
        panel = serializer.instance.panel
        if not self._user_has_panel_access(panel):
            raise serializers.ValidationError("User cannot update schedules for this panel")
        schedule = serializer.save()
        log_audit_event(
            actor=self.request.user,
            panel=panel,
            action=AuditLog.Action.UPDATE,
            instance=schedule,
            description="Report schedule updated",
            request=self.request,
        )

    def perform_destroy(self, instance):
        if not self._user_has_panel_access(instance.panel):
            raise serializers.ValidationError("User cannot delete schedules for this panel")
        log_audit_event(
            actor=self.request.user,
            panel=instance.panel,
            action=AuditLog.Action.DELETE,
            instance=instance,
            description="Report schedule deleted",
            request=self.request,
        )
        instance.delete()

    @action(detail=True, methods=["post"])
    def run_now(self, request, id=None):
        schedule = self.get_object()
        if not self._user_has_panel_access(schedule.panel):
            return Response({"detail": "Access denied"}, status=status.HTTP_403_FORBIDDEN)

        advance_report_schedule(schedule, executed_at=now())
        log_audit_event(
            actor=request.user,
            panel=schedule.panel,
            action=AuditLog.Action.RUN_SCHEDULE,
            instance=schedule,
            description="Report schedule run manually",
            request=request,
        )

        return Response(
            {
                "detail": "Schedule marked as executed",
                "schedule_id": schedule.id,
                "last_run_at": schedule.last_run_at,
                "next_run_at": schedule.next_run_at,
            }
        )

    def _user_has_panel_access(self, panel):
        if panel.owner == self.request.user:
            return True
        return PanelUser.objects.filter(user=self.request.user, panel=panel).exists()


class WebhookViewSet(viewsets.ModelViewSet):
    """Manage webhooks for panels."""

    serializer_class = None
    permission_classes = [IsAuthenticated, IsPanelOwnerOrEditor]
    lookup_field = "id"

    def __init__(self, *args, **kwargs):
        from .serializers import WebhookSerializer

        self.serializer_class = WebhookSerializer
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        # return webhooks for panels where the user is a member or owner
        user_panel_ids = PanelUser.objects.filter(user=self.request.user).values_list("panel_id", flat=True)
        owner_panel_ids = Panel.objects.filter(owner=self.request.user).values_list("id", flat=True)
        panels = list(user_panel_ids) + list(owner_panel_ids)
        from .models import Webhook

        return Webhook.objects.filter(panel_id__in=panels).order_by("-created_at")

    def perform_create(self, serializer):
        panel = serializer.validated_data.get("panel")
        if not self._user_can_edit_panel(panel):
            raise serializers.ValidationError("User cannot create webhooks for this panel")
        # generate secret if not provided
        w = serializer.save()
        if not w.secret:
            import secrets

            w.secret = secrets.token_urlsafe(32)
            w.save(update_fields=["secret"]) 

    def _user_can_edit_panel(self, panel):
        if panel.owner == self.request.user:
            return True
        try:
            membership = PanelUser.objects.get(user=self.request.user, panel=panel)
            return membership.role == PanelUser.Role.EDITOR
        except PanelUser.DoesNotExist:
            return False

    @action(detail=True, methods=["post"])
    def test_send(self, request, id=None):
        """Send a test payload to the webhook asynchronously."""
        webhook = self.get_object()
        payload = request.data.get("payload") or {"test": True}
        from .tasks import send_webhook_event

        task = send_webhook_event.delay(str(webhook.id), payload)
        return Response({"task_id": task.id})


class RecurringExpenseViewSet(viewsets.ModelViewSet):
    """Recurring expense management within panels."""

    serializer_class = None
    permission_classes = [IsAuthenticated, IsPanelMemberReadOnly, ViewerReadOnly]
    lookup_field = "id"

    def __init__(self, *args, **kwargs):
        from .serializers import RecurringExpenseSerializer

        self.serializer_class = RecurringExpenseSerializer
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        """Return recurring expenses for user's panels."""
        user_panel_ids = PanelUser.objects.filter(user=self.request.user).values_list("panel_id", flat=True)
        user_owned_panel_ids = Panel.objects.filter(owner=self.request.user).values_list("id", flat=True)
        all_panel_ids = list(user_panel_ids) + list(user_owned_panel_ids)
        from .models import RecurringExpense

        return RecurringExpense.objects.filter(panel_id__in=all_panel_ids).order_by("-created_at")

    def perform_create(self, serializer):
        """Set created_by to current user."""
        panel = serializer.validated_data.get("panel")
        if not self._user_can_edit_panel(panel):
            raise serializers.ValidationError("User cannot create recurring expenses in this panel")
        recurring = serializer.save(created_by=self.request.user)
        log_audit_event(
            actor=self.request.user,
            panel=panel,
            action=AuditLog.Action.CREATE,
            instance=recurring,
            description="Recurring expense created",
            request=self.request,
        )

    def perform_update(self, serializer):
        """Allow editor/owner to update."""
        if not self._user_can_edit_panel(serializer.instance.panel):
            raise serializers.ValidationError("User cannot update recurring expenses in this panel")
        recurring = serializer.save()
        log_audit_event(
            actor=self.request.user,
            panel=recurring.panel,
            action=AuditLog.Action.UPDATE,
            instance=recurring,
            description="Recurring expense updated",
            request=self.request,
        )

    def perform_destroy(self, instance):
        """Allow editor/owner to delete."""
        if not self._user_can_edit_panel(instance.panel):
            raise serializers.ValidationError("User cannot delete recurring expenses in this panel")
        log_audit_event(
            actor=self.request.user,
            panel=instance.panel,
            action=AuditLog.Action.DELETE,
            instance=instance,
            description="Recurring expense deleted",
            request=self.request,
        )
        instance.delete()

    def _user_can_edit_panel(self, panel):
        if panel.owner == self.request.user:
            return True
        try:
            membership = PanelUser.objects.get(user=self.request.user, panel=panel)
            return membership.role == PanelUser.Role.EDITOR
        except PanelUser.DoesNotExist:
            return False


class CategoryViewSet(viewsets.ModelViewSet):
    """Category management within panels."""

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsPanelMemberReadOnly, ViewerReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        """Return categories for user's panels."""
        user_panel_ids = PanelUser.objects.filter(user=self.request.user).values_list("panel_id", flat=True)
        user_owned_panel_ids = Panel.objects.filter(owner=self.request.user).values_list("id", flat=True)
        all_panel_ids = list(user_panel_ids) + list(user_owned_panel_ids)
        return Category.objects.filter(panel_id__in=all_panel_ids).order_by("-created_at", "name")

    def perform_create(self, serializer):
        """Ensure panel belongs to user."""
        panel = serializer.validated_data.get("panel")
        if not self._user_can_edit_panel(panel):
            raise serializers.ValidationError("User cannot create categories in this panel")
        category = serializer.save()
        log_audit_event(
            actor=self.request.user,
            panel=panel,
            action=AuditLog.Action.CREATE,
            instance=category,
            description="Category created",
            request=self.request,
        )

    def perform_update(self, serializer):
        """Ensure user has permission."""
        if not self._user_can_edit_panel(serializer.instance.panel):
            raise serializers.ValidationError("User cannot update categories in this panel")
        category = serializer.save()
        log_audit_event(
            actor=self.request.user,
            panel=category.panel,
            action=AuditLog.Action.UPDATE,
            instance=category,
            description="Category updated",
            request=self.request,
        )

    def perform_destroy(self, instance):
        """Ensure user has permission."""
        if not self._user_can_edit_panel(instance.panel):
            raise serializers.ValidationError("User cannot delete categories in this panel")
        log_audit_event(
            actor=self.request.user,
            panel=instance.panel,
            action=AuditLog.Action.DELETE,
            instance=instance,
            description="Category deleted",
            request=self.request,
        )
        instance.delete()

    def _user_can_edit_panel(self, panel):
        if panel.owner == self.request.user:
            return True
        try:
            membership = PanelUser.objects.get(user=self.request.user, panel=panel)
            return membership.role == PanelUser.Role.EDITOR
        except PanelUser.DoesNotExist:
            return False


class ExpenseViewSet(viewsets.ModelViewSet):
    """Expense management within panels."""

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsPanelMemberReadOnly, ViewerReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        """Return expenses for user's panels, excluding soft-deleted."""
        user_panel_ids = PanelUser.objects.filter(user=self.request.user).values_list("panel_id", flat=True)
        user_owned_panel_ids = Panel.objects.filter(owner=self.request.user).values_list("id", flat=True)
        all_panel_ids = list(user_panel_ids) + list(user_owned_panel_ids)
        return Expense.objects.filter(panel_id__in=all_panel_ids, deleted_at__isnull=True).order_by("-created_at")

    def perform_create(self, serializer):
        """Set created_by to current user."""
        panel = serializer.validated_data.get("panel")
        if not self._user_can_edit_panel(panel):
            raise serializers.ValidationError("User cannot create expenses in this panel")
        expense = serializer.save(created_by=self.request.user)
        log_audit_event(
            actor=self.request.user,
            panel=panel,
            action=AuditLog.Action.CREATE,
            instance=expense,
            description="Expense created",
            request=self.request,
        )

        # After saving expense, evaluate budgets and create notifications if thresholds crossed.
        try:
            from django.db.models import Sum

            related_budgets = Budget.objects.filter(panel=panel)
            for budget in related_budgets:
                qs = Expense.objects.filter(panel=panel, deleted_at__isnull=True)
                if budget.category_id:
                    qs = qs.filter(category=budget.category)
                if budget.start_date:
                    qs = qs.filter(date__gte=budget.start_date)
                if budget.end_date:
                    qs = qs.filter(date__lte=budget.end_date)

                # compute previous spent excluding the newly created expense
                previous_spent = qs.exclude(id=expense.id).aggregate(total=Sum("amount"))["total"] or Decimal("0")
                spent = previous_spent + (expense.amount or Decimal("0"))

                threshold_amount = (budget.limit_amount * Decimal(budget.alert_threshold)) / Decimal("100")

                # Warning threshold crossed
                if previous_spent < threshold_amount <= spent:
                    # notify panel members who opted in
                    prefs = NotificationPreference.objects.filter(panel=panel, type=Notification.Type.BUDGET_WARNING, enabled=True)
                    for pref in prefs:
                        notification = Notification.objects.create(
                            user=pref.user,
                            panel=panel,
                            type=Notification.Type.BUDGET_WARNING,
                            message=f"Budget '{budget}' reached {budget.alert_threshold}% ({spent}/{budget.limit_amount})",
                        )
                        if pref.delivery == NotificationPreference.Delivery.EMAIL:
                            send_notification_email.delay(str(notification.id))

                # Budget exceeded
                if previous_spent < budget.limit_amount <= spent:
                    prefs = NotificationPreference.objects.filter(panel=panel, type=Notification.Type.BUDGET_EXCEEDED, enabled=True)
                    for pref in prefs:
                        notification = Notification.objects.create(
                            user=pref.user,
                            panel=panel,
                            type=Notification.Type.BUDGET_EXCEEDED,
                            message=f"Budget '{budget}' exceeded ({spent}/{budget.limit_amount})",
                        )
                        if pref.delivery == NotificationPreference.Delivery.EMAIL:
                            send_notification_email.delay(str(notification.id))
        except Exception:
            # Do not block expense creation on notification errors
            pass
        # enqueue webhook notifications for expense.created
        try:
            payload = {
                "event": "expense.created",
                "expense_id": str(expense.id),
                "panel_id": str(panel.id),
                "amount": str(expense.amount),
                "date": expense.date.isoformat(),
                "created_by": str(expense.created_by.id),
            }
            notify_webhooks.delay(str(panel.id), "expense.created", payload)
        except Exception:
            pass

    def perform_update(self, serializer):
        """Allow editor/owner to update."""
        if not self._user_can_edit_panel(serializer.instance.panel):
            raise serializers.ValidationError("User cannot update expenses in this panel")
        expense = serializer.save()
        log_audit_event(
            actor=self.request.user,
            panel=expense.panel,
            action=AuditLog.Action.UPDATE,
            instance=expense,
            description="Expense updated",
            request=self.request,
        )

    def perform_destroy(self, instance):
        """Soft delete expense."""
        if not self._user_can_edit_panel(instance.panel):
            raise serializers.ValidationError("User cannot delete expenses in this panel")
        instance.deleted_at = now()
        instance.save()
        log_audit_event(
            actor=self.request.user,
            panel=instance.panel,
            action=AuditLog.Action.DELETE,
            instance=instance,
            description="Expense soft-deleted",
            request=self.request,
        )

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        """Get expenses grouped by category."""
        panel_id = request.query_params.get("panel_id")
        if not panel_id:
            return Response(
                {"detail": "panel_id query param required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            panel = Panel.objects.get(id=panel_id)
        except Panel.DoesNotExist:
            return Response(
                {"detail": "Panel not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not self._user_has_panel_access(panel):
            return Response(
                {"detail": "Access denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        categories = Category.objects.filter(panel=panel)
        result = {}
        for category in categories:
            expenses = Expense.objects.filter(panel=panel, category=category, deleted_at__isnull=True)
            result[category.name] = ExpenseSerializer(expenses, many=True).data

        return Response(result)

    def _user_can_edit_panel(self, panel):
        if panel.owner == self.request.user:
            return True
        try:
            membership = PanelUser.objects.get(user=self.request.user, panel=panel)
            return membership.role == PanelUser.Role.EDITOR
        except PanelUser.DoesNotExist:
            return False

    def _user_has_panel_access(self, panel):
        if panel.owner == self.request.user:
            return True
        return PanelUser.objects.filter(user=self.request.user, panel=panel).exists()


class BudgetViewSet(viewsets.ModelViewSet):
    """Budget management within panels."""

    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated, IsPanelMemberReadOnly, ViewerReadOnly]
    lookup_field = "id"

    def get_queryset(self):
        """Return budgets for user's panels."""
        user_panel_ids = PanelUser.objects.filter(user=self.request.user).values_list("panel_id", flat=True)
        user_owned_panel_ids = Panel.objects.filter(owner=self.request.user).values_list("id", flat=True)
        all_panel_ids = list(user_panel_ids) + list(user_owned_panel_ids)
        return Budget.objects.filter(panel_id__in=all_panel_ids).order_by("-created_at")

    def perform_create(self, serializer):
        """Ensure user has editor+ permissions."""
        panel = serializer.validated_data.get("panel")
        if not self._user_can_edit_panel(panel):
            raise serializers.ValidationError("User cannot create budgets in this panel")
        budget = serializer.save()
        log_audit_event(
            actor=self.request.user,
            panel=panel,
            action=AuditLog.Action.CREATE,
            instance=budget,
            description="Budget created",
            request=self.request,
        )

    def perform_update(self, serializer):
        """Allow editor/owner to update."""
        if not self._user_can_edit_panel(serializer.instance.panel):
            raise serializers.ValidationError("User cannot update budgets in this panel")
        budget = serializer.save()
        log_audit_event(
            actor=self.request.user,
            panel=budget.panel,
            action=AuditLog.Action.UPDATE,
            instance=budget,
            description="Budget updated",
            request=self.request,
        )

    def perform_destroy(self, instance):
        """Allow editor/owner to delete."""
        if not self._user_can_edit_panel(instance.panel):
            raise serializers.ValidationError("User cannot delete budgets in this panel")
        log_audit_event(
            actor=self.request.user,
            panel=instance.panel,
            action=AuditLog.Action.DELETE,
            instance=instance,
            description="Budget deleted",
            request=self.request,
        )
        instance.delete()

    @action(detail=False, methods=["get"])
    def check_status(self, request):
        """Check budget status (spent vs limit)."""
        panel_id = request.query_params.get("panel_id")
        if not panel_id:
            return Response(
                {"detail": "panel_id query param required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            panel = Panel.objects.get(id=panel_id)
        except Panel.DoesNotExist:
            return Response(
                {"detail": "Panel not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not self._user_has_panel_access(panel):
            return Response(
                {"detail": "Access denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        budgets = Budget.objects.filter(panel=panel)
        result = []
        for budget in budgets:
            if budget.category:
                spent = Expense.objects.filter(
                    panel=panel,
                    category=budget.category,
                    deleted_at__isnull=True,
                ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
            else:
                spent = Expense.objects.filter(panel=panel, deleted_at__isnull=True).aggregate(
                    total=Sum("amount")
                )["total"] or Decimal("0")

            status_info = "on_track"
            if spent >= budget.limit_amount:
                status_info = "exceeded"
            elif (spent * Decimal("100") / budget.limit_amount) >= budget.alert_threshold:
                status_info = "warning"

            result.append(
                {
                    "budget_id": budget.id,
                    "limit": budget.limit_amount,
                    "spent": spent,
                    "status": status_info,
                }
            )

        return Response(result)

    def _user_can_edit_panel(self, panel):
        if panel.owner == self.request.user:
            return True
        try:
            membership = PanelUser.objects.get(user=self.request.user, panel=panel)
            return membership.role == PanelUser.Role.EDITOR
        except PanelUser.DoesNotExist:
            return False

    def _user_has_panel_access(self, panel):
        if panel.owner == self.request.user:
            return True
        return PanelUser.objects.filter(user=self.request.user, panel=panel).exists()


class NotificationViewSet(viewsets.ModelViewSet):
    """Notification management."""

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        """Return notifications for current user."""
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

    @action(detail=False, methods=["get"])
    def unread(self, request):
        """Get unread notifications."""
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by("-created_at")
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def mark_as_read(self, request, id=None):
        """Mark a notification as read."""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response(NotificationSerializer(notification).data)

    @action(detail=False, methods=["patch"])
    def mark_all_as_read(self, request):
        """Mark all notifications as read for current user."""
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({"detail": "All notifications marked as read"})
