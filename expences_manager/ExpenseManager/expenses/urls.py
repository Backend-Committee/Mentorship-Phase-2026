from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BudgetViewSet,
    CategoryViewSet,
    ExpenseViewSet,
    NotificationViewSet,
    ReportSummaryView,
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
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"panels", PanelViewSet, basename="panel")
router.register(r"panel-users", PanelUserViewSet, basename="panel-user")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"expenses", ExpenseViewSet, basename="expense")
router.register(r"budgets", BudgetViewSet, basename="budget")
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(r"notification-preferences", NotificationPreferenceViewSet, basename="notification-preference")

urlpatterns = [
    # Authentication endpoints
    path("auth/register/", UserRegistrationView.as_view(), name="register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshViewCustom.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="auth-logout"),
    path("auth/password_reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("auth/password_reset_confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("reports/summary/", ReportSummaryView.as_view(), name="report-summary"),
    path("invitations/accept/", InvitationAcceptView.as_view(), name="invitation-accept"),
    # DRF router endpoints
    path("", include(router.urls)),
]
