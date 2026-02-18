"""
URL configuration for mainSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

# according to two scoops book (an amazing book for django)
# you should explain what an app do in one sentence or less, if you're using and's then you have to split it into multiple apps.
# now for our project 
# Project Features
# Product Management
    # Add new products
    # Update product details (price, stock, availability)
    # Delete products
    # View all products
# all the above are under the same category of product management.

# Category System
    # Create categories
    # Assign products to categories
    # Filter products by category
# Search & Filter
    # Search products by name
    # Filter by category
    # Display only available products
# Shopping Cart
    # Add products to cart
    # Select quantity
    # Prevent orders exceeding stock
    # View cart items
# Admin Panel
    # Manage products and categories through Django Admin
    # Use search, filter, and list display features


# which means four apps other than the main project app(mainSite)
urlpatterns = [
    path('admin/', admin.site.urls),
]
