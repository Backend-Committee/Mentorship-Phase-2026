"""
URL configuration for BankSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers as drf_routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.views import UserViewSet, RegisterView
from accounts.views import AccountViewSet
from transactions.views import TransactionViewSet
from payments.views import PaymentViewSet
from approvals.views import ApprovalRequestViewSet
from audit.views import AuditLogViewSet

# Mobile Router (Customer Facing)
mobile_router = drf_routers.DefaultRouter()
mobile_router.register(r'users', UserViewSet, basename='mobile-users')
mobile_router.register(r'accounts', AccountViewSet, basename='mobile-accounts')
mobile_router.register(r'transactions', TransactionViewSet, basename='mobile-transactions')
mobile_router.register(r'payments', PaymentViewSet, basename='mobile-payments')

# Office Router (Staff Facing)
office_router = drf_routers.DefaultRouter()
office_router.register(r'users', UserViewSet, basename='office-users')
office_router.register(r'accounts', AccountViewSet, basename='office-accounts')
office_router.register(r'transactions', TransactionViewSet, basename='office-transactions')
office_router.register(r'approvals', ApprovalRequestViewSet, basename='approvals')
office_router.register(r'audit', AuditLogViewSet, basename='audit')

schema_view = get_schema_view(
   openapi.Info(
      title="Bank System API",
      default_version='v1',
      description="API documentation for the Banking System (Mobile & Office)",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@banksystem.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    
    # Auth
    path('api/auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Mobile API
    path('api/mobile/', include(mobile_router.urls)),

    # Office API
    path('api/office/', include(office_router.urls)),
]

