from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (
    BudgetViewSet,
    CategoryViewSet,
    ExpenseViewSet,
    NotificationViewSet,
    AuditLogViewSet,
    ReportMonthlyView,
    ReportScheduleViewSet,
    ReportSummaryView,
    ReportTrendsView,
    InvitationAcceptView,
    NotificationPreferenceViewSet,
    LogoutView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    PanelUserViewSet,
    PanelViewSet,
    CustomTokenObtainPairView,
    TokenRefreshViewCustom,
    UserRegistrationView,
    UserViewSet,
    WebhookViewSet,
    RecurringExpenseViewSet,
)

# Accept both slash and non-slash forms (e.g. /api/panels and /api/panels/).
router = DefaultRouter()
router.trailing_slash = '/?'
router.register(r"users", UserViewSet, basename="user")
router.register(r"panels", PanelViewSet, basename="panel")
router.register(r"panel-users", PanelUserViewSet, basename="panel-user")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"expenses", ExpenseViewSet, basename="expense")
router.register(r"recurring-expenses", RecurringExpenseViewSet, basename="recurring-expense")
router.register(r"budgets", BudgetViewSet, basename="budget")
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"notification-preferences", NotificationPreferenceViewSet, basename="notification-preference")
router.register(r"report-schedules", ReportScheduleViewSet, basename="report-schedule")
router.register(r"audit-logs", AuditLogViewSet, basename="audit-log")
router.register(r"webhooks", WebhookViewSet, basename="webhook")

urlpatterns = [
    # Authentication endpoints
    re_path(r"^auth/register/?$", UserRegistrationView.as_view(), name="register"),
    re_path(r"^auth/login/?$", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    re_path(r"^auth/refresh/?$", TokenRefreshViewCustom.as_view(), name="token_refresh"),
    re_path(r"^auth/logout/?$", LogoutView.as_view(), name="auth-logout"),
    re_path(r"^auth/password_reset/?$", PasswordResetRequestView.as_view(), name="password-reset"),
    re_path(r"^auth/password_reset_confirm/?$", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    re_path(r"^reports/summary/?$", ReportSummaryView.as_view(), name="report-summary"),
    re_path(r"^reports/monthly/?$", ReportMonthlyView.as_view(), name="report-monthly"),
    re_path(r"^reports/trends/?$", ReportTrendsView.as_view(), name="report-trends"),
    re_path(r"^invitations/accept/?$", InvitationAcceptView.as_view(), name="invitation-accept"),
    # DRF router endpoints
    path("", include(router.urls)),
]

# API versioning (supports /api/v1/ and /api/ prefixes)
from rest_framework_simplejwt.views import TokenVerifyView

app_urlpatterns = [
    re_path(r"^auth/token/verify/?$", TokenVerifyView.as_view(), name="token_verify"),
] + urlpatterns
