from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.product_List, name='product_List'),
    path('addpro/', views.addpro, name='addpro'),
    path('update/<int:pk>/', views.Updatepro, name='update_pro'),
    path('delete/<int:pk>/', views.delete_product, name='delete_pro'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)