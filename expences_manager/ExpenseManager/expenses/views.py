import csv
from decimal import Decimal
from io import StringIO

from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Count, Max, Min, Sum
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

from .models import Budget, Category, Expense, Notification, Panel, PanelUser, User
from .models import Invitation, NotificationPreference
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
    InvitationSerializer,
)


class UserRegistrationView(APIView):
    """Register a new user."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
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
        if export_format == "csv":
            return self._render_csv(payload)
        return Response(payload)

    def _render_csv(self, payload):
        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["section", "name", "value"])
        writer.writerow(["panel", "id", payload["panel"]["id"]])
        writer.writerow(["panel", "name", payload["panel"]["name"]])
        writer.writerow(["expenses", "count", payload["expenses"]["count"]])
        writer.writerow(["expenses", "total_spent", payload["expenses"]["total_spent"]])
        writer.writerow(["expenses", "first_expense_date", payload["expenses"]["first_expense_date"]])
        writer.writerow(["expenses", "last_expense_date", payload["expenses"]["last_expense_date"]])
        for row in payload["expenses"]["by_category"]:
            writer.writerow(["category", row["category_name"], row["total_spent"]])
        for row in payload["budgets"]:
            writer.writerow(["budget", row["budget_id"], row["status"]])

        response = HttpResponse(buffer.getvalue(), content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="report-summary.csv"'
        return response

    def _build_cache_key(self, user_id, panel_id, date_from, date_to, export_format):
        return f"report-summary:{user_id}:{panel_id}:{date_from or ''}:{date_to or ''}:{export_format}"

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
        return Panel.objects.filter(id__in=user_panels) | Panel.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Set owner to current user."""
        serializer.save(owner=self.request.user)
        panel = serializer.instance
        PanelUser.objects.create(user=self.request.user, panel=panel, role=PanelUser.Role.OWNER, joined_at=now())

    def perform_update(self, serializer):
        """Only owner can update."""
        if serializer.instance.owner != self.request.user:
            raise serializers.ValidationError("Only panel owner can update.")
        serializer.save()

    def perform_destroy(self, instance):
        """Only owner can delete."""
        if instance.owner != self.request.user:
            raise serializers.ValidationError("Only panel owner can delete.")
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

            return Response(InvitationSerializer(invitation).data, status=status.HTTP_201_CREATED)

        return Response({"detail": "user_id or email is required"}, status=status.HTTP_400_BAD_REQUEST)


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
        return NotificationPreference.objects.filter(user=self.request.user, panel_id__in=all_panel_ids)

    def perform_create(self, serializer):
        # Ensure the preference belongs to the requesting user
        serializer.save(user=self.request.user)


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
        return Category.objects.filter(panel_id__in=all_panel_ids)

    def perform_create(self, serializer):
        """Ensure panel belongs to user."""
        panel = serializer.validated_data.get("panel")
        if not self._user_can_edit_panel(panel):
            raise serializers.ValidationError("User cannot create categories in this panel")
        serializer.save()

    def perform_update(self, serializer):
        """Ensure user has permission."""
        if not self._user_can_edit_panel(serializer.instance.panel):
            raise serializers.ValidationError("User cannot update categories in this panel")
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure user has permission."""
        if not self._user_can_edit_panel(instance.panel):
            raise serializers.ValidationError("User cannot delete categories in this panel")
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
        return Expense.objects.filter(panel_id__in=all_panel_ids, deleted_at__isnull=True)

    def perform_create(self, serializer):
        """Set created_by to current user."""
        panel = serializer.validated_data.get("panel")
        if not self._user_can_edit_panel(panel):
            raise serializers.ValidationError("User cannot create expenses in this panel")
        expense = serializer.save(created_by=self.request.user)

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
                        Notification.objects.create(
                            user=pref.user,
                            panel=panel,
                            type=Notification.Type.BUDGET_WARNING,
                            message=f"Budget '{budget}' reached {budget.alert_threshold}% ({spent}/{budget.limit_amount})",
                        )

                # Budget exceeded
                if previous_spent < budget.limit_amount <= spent:
                    prefs = NotificationPreference.objects.filter(panel=panel, type=Notification.Type.BUDGET_EXCEEDED, enabled=True)
                    for pref in prefs:
                        Notification.objects.create(
                            user=pref.user,
                            panel=panel,
                            type=Notification.Type.BUDGET_EXCEEDED,
                            message=f"Budget '{budget}' exceeded ({spent}/{budget.limit_amount})",
                        )
        except Exception:
            # Do not block expense creation on notification errors
            pass

    def perform_update(self, serializer):
        """Allow editor/owner to update."""
        if not self._user_can_edit_panel(serializer.instance.panel):
            raise serializers.ValidationError("User cannot update expenses in this panel")
        serializer.save()

    def perform_destroy(self, instance):
        """Soft delete expense."""
        if not self._user_can_edit_panel(instance.panel):
            raise serializers.ValidationError("User cannot delete expenses in this panel")
        instance.deleted_at = now()
        instance.save()

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
        return Budget.objects.filter(panel_id__in=all_panel_ids)

    def perform_create(self, serializer):
        """Ensure user has editor+ permissions."""
        panel = serializer.validated_data.get("panel")
        if not self._user_can_edit_panel(panel):
            raise serializers.ValidationError("User cannot create budgets in this panel")
        serializer.save()

    def perform_update(self, serializer):
        """Allow editor/owner to update."""
        if not self._user_can_edit_panel(serializer.instance.panel):
            raise serializers.ValidationError("User cannot update budgets in this panel")
        serializer.save()

    def perform_destroy(self, instance):
        """Allow editor/owner to delete."""
        if not self._user_can_edit_panel(instance.panel):
            raise serializers.ValidationError("User cannot delete budgets in this panel")
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
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get"])
    def unread(self, request):
        """Get unread notifications."""
        notifications = Notification.objects.filter(user=request.user, is_read=False)
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
