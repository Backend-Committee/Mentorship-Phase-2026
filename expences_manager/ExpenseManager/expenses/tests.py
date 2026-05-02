from datetime import date
from decimal import Decimal

from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from .models import Budget, Category, Expense, Invitation, Notification, Panel, PanelUser, User
from .views import ReportSummaryView


class AuthAndInvitationApiTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@example.com",
            password="StrongPass123",
        )
        self.panel = Panel.objects.create(name="Main Panel", owner=self.owner)
        PanelUser.objects.create(user=self.owner, panel=self.panel, role=PanelUser.Role.OWNER)

    def test_login_returns_panel_claims(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            {
                "username": "owner",
                "password": "StrongPass123",
                "panel_id": str(self.panel.id),
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user_id"], str(self.owner.id))
        self.assertEqual(response.data["panel_id"], str(self.panel.id))
        self.assertEqual(response.data["role"], PanelUser.Role.OWNER)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invitation_acceptance_creates_membership(self):
        invited_user = User.objects.create_user(
            username="member",
            email="member@example.com",
            password="StrongPass123",
        )
        invitation = Invitation.objects.create(
            panel=self.panel,
            email=invited_user.email,
            token="invite-token-123",
            role=PanelUser.Role.VIEWER,
            invited_by=self.owner,
        )

        self.client.force_authenticate(user=invited_user)
        response = self.client.post(
            reverse("invitation-accept"),
            {"token": invitation.token},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(PanelUser.objects.filter(user=invited_user, panel=self.panel).exists())
        invitation.refresh_from_db()
        self.assertIsNotNone(invitation.accepted_at)
        self.assertEqual(Notification.objects.filter(user=invited_user, panel=self.panel).count(), 1)


class ReportApiTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(
            username="reporter",
            email="reporter@example.com",
            password="StrongPass123",
        )
        self.panel = Panel.objects.create(name="Finance", owner=self.user)
        PanelUser.objects.create(user=self.user, panel=self.panel, role=PanelUser.Role.OWNER)
        self.category = Category.objects.create(panel=self.panel, name="Food")
        Budget.objects.create(
            panel=self.panel,
            category=None,
            limit_amount=Decimal("100.00"),
            period=Budget.Period.MONTHLY,
            alert_threshold=80,
        )
        Expense.objects.create(
            panel=self.panel,
            category=self.category,
            created_by=self.user,
            amount=Decimal("12.50"),
            date=date.today(),
            description="Lunch",
        )

    def test_report_summary_csv_export(self):
        factory = APIRequestFactory()
        request = factory.get(
            "/api/reports/summary/",
            {"panel_id": str(self.panel.id), "export": "csv"},
        )
        force_authenticate(request, user=self.user)
        response = ReportSummaryView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("attachment; filename=\"report-summary.csv\"", response["Content-Disposition"])
        self.assertIn("expenses,count", response.content.decode())
