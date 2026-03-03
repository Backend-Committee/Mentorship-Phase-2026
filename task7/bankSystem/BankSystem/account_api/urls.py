from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import  TokenObtainPairView, TokenRefreshView


from .views import BankAccountList, BankAccountDetail, BankAccountUserList, UserList, UserDetail, TransactionViewSet, TransactionDetailView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path("bankaccount/", BankAccountList.as_view(), name="bankaccount-list"),
    path("bankaccount/me/", BankAccountUserList.as_view(), name="bankaccount-me"),
    path("bankaccount/<int:pk>/", BankAccountDetail.as_view(), name="bankaccount-detail"),
    path("user/", UserList.as_view(), name="user-list"),
    path("user/<int:pk>/", UserDetail.as_view(), name="user-detail"),
    path('transactions/', TransactionViewSet.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)