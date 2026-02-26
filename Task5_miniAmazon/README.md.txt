Amazon Mini 🛒
A lightweight Django-based e-commerce web application for browsing, managing, and purchasing products across categories like Tea, Coffee, and Juice.

Features

User Login — Simple session-based login (no registration required)
Product Store — Browse products with images, prices, stock levels, and categories
Search & Filter — Search by name and filter by category in real time
Shopping Cart — Add products to cart with quantity control; stock is updated automatically
Product Management — Add, update, and delete products via the UI
Stock Tracking — Each product has a live stock count; overselling is prevented


Project Structure
project/
├── models.py        # Product, Category, Login models
├── views.py         # All view logic (home, store, cart, CRUD)
├── urls.py          # URL routing
├── form.py          # Django form for adding/updating products
└── templates/
    └── pages/
        ├── home.html        # Login page
        ├── product.html     # Store / product listing
        ├── AddPro.html      # Add product form
        ├── update.html      # Update product form
        └── cart.html        # Shopping cart view
    └── base.html            # Shared navbar and layout

Models
ModelKey Fieldsproductname, price, category, image, Is_Available, stockCategorynameloginusername, password

URL Routes
URLViewDescription/homeLogin page/store/product_ListProduct listing/addpro/addproAdd a new product/update/<pk>/UpdateproUpdate an existing product/delete/<pk>/delete_productDelete a product/cart/add/<pk>/add_to_cartAdd product to cart/cart/view_cartView shopping cart

Getting Started
Prerequisites

Python 3.8+
Django 4.x
Pillow (for image uploads)

Installation
bash# 1. Clone the repository
git clone <repo-url>
cd <project-folder>

# 2. Install dependencies
pip install django pillow

# 3. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 4. Run the development server
python manage.py runserver
Then open your browser and go to http://127.0.0.1:8000/
Media Files
Add the following to your settings.py to enable image uploads:
pythonMEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

Usage

Login — Enter any username and password on the home page to start a session.
Browse — Visit the Store to see all available products.
Search/Filter — Use the search bar or category dropdown to narrow results.
Add to Cart — Choose a quantity and click "Add". Stock is checked before adding.
View Cart — See all cart items, quantities, subtotals, and the total price.
Manage Products — Use Add / Update / Delete buttons to manage the catalog.


Tech Stack

Backend: Django (Python)
Frontend: Bootstrap 5
Database: SQLite (default)
Sessions: Django built-in session framework


Color Theme
ElementColorNavbar#800000 (Maroon)Accent text#FFC0CB (Pink)Background#fff5f6

Notes

This project uses a simple custom login model (not Django's built-in auth system).
Passwords are stored in plain text — not suitable for production use.
For production, consider using django.contrib.auth and adding HTTPS.