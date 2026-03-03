from django.urls import path
from . import views
urlpatterns = [
    path('customers/', views.ListCreateCustomers.as_view() , name='customers'),
    path('customers/<int:pk>' , views.DeleteUpdateCustomer.as_view() , name='customer-detail'),
]
