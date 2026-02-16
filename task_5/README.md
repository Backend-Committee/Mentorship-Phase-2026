# Mini Amazon - E-Commerce Platform

A lightweight Django-based e-commerce application that mimics core Amazon functionality including product browsing, filtering, searching, and shopping cart management.

## Features

- **Search & Filter**: Search products by name and filter by category, also
- **Availability Filter**: Display only in-stock products
- **Shopping Cart**: Add/remove items from cart with dynamic quantity management
- **Order Management**: Place orders with automatic inventory updates
- **Admin Dashboard**: Django admin interface for managing products and categories

## How to use it ?
- just run the server and you are ready to go, the database is already filled initially for you

- The database have some categories and products, but you can always create new ones (also editing the stock) by using django admin.

- currently only one image can be added to each product, save the image in the static folder in the suitable place following the existing products pattern, also add its name like 'image.png' to product data from django admin