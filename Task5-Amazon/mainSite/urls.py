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
from django.urls import include, path

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


# which means four apps other than the main project app(mainSite) are needed to be created

# even if the project is small, it's better to split it into multiple apps for better organization and maintainability.
# if i found out that one app is too small, i can always just merge it with another app, so all is fine for now.

# sites needed
# home page (which will show all the products and categories)
    # has search bar in the header
    # has a hamburger menu in the header which will show the categories and the cart
# we need a page for each category which will show the products in that category
# we need a page for the cart which will show the products in the cart and the total price and the checkout button
# we need a page for the search results which will show the products that match the search query
    # the search page would have an aside that will show all filters we can use
# and of course the product detail page which will show the product details and the add to cart button
# we need a page for the admin panel which will show the products and categories and allow us to manage them 

# ....

# ok, so, as you can clearly see, i just made a layout for a frontend website project. which sadly, is not what i need in here.
# old habits die hard i guess

# for now, make the crud operations for the products and categories, and then we can move on to the cart and search features, which are a bit more complex.
# in the admin panel, we can manage the products and categories.
# anything else we can make into a standalone api endpoint, that takes the needed filters and returns the needed data, and then we can connect it to the frontend later on.

# Todo: try to connect this to the other amazon react project you made.
urlpatterns = [
    path('', include('products.urls')),
    # would contain the home page and the  
    # path('categories/', include('categories.urls')),
    path('cart/', include('cart.urls')),
    # path('search/', include('search.urls')),
    path('admin/', admin.site.urls),
]

