
from django.contrib import admin
from django.urls import path, include

app_name = 'BankAccount'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls'),name='account'),
    path('api/', include('account_api.urls'),name='account_api'),
]
