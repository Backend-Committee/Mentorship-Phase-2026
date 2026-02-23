# Amazon Pro Project — Setup Guide

## 1. Install dependencies

```bash
pip install django requests
```

## 2. Add to INSTALLED_APPS in settings.py

```python
INSTALLED_APPS = [
    ...
    'store',
]
```

## 3. Add to your main urls.py

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]
```

## 4. Add session settings to settings.py (already on by default, just confirm)

```python
# These should already be in your settings.py
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
```

## 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6. Create a superuser (for admin panel)

```bash
python manage.py createsuperuser
```

## 7. Seed the database

```bash
pip install requests   # if not already installed
python manage.py seed_products
```

## 8. (Optional) Save as fixture for reuse

```bash
python manage.py dumpdata store.Product store.Category --indent 2 > store/fixtures/products.json
```

## 9. (Optional) Load fixture instead of seeding

```bash
python manage.py loaddata products.json
```

## 10. Run the server

```bash
python manage.py runserver
```

## File structure

```
store/
├── models.py              # Product, Category, Cart, CartItem
├── views.py               # All views (product CRUD + cart)
├── forms.py               # ProductForm + AddToCartForm
├── urls.py                # All URL patterns
├── admin.py               # Customized admin panel
├── management/
│   └── commands/
│       └── seed_products.py   # Fetches from fakestoreapi
└── templates/
    └── store/
        ├── base.html
        ├── product_list.html
        ├── product_detail.html
        ├── product_form.html          (add + update)
        ├── product_confirm_delete.html
        ├── cart.html
        ├── cart_add.html
        └── cart_update.html
```

## Features covered

- Product CRUD (Add/Update/Delete protected to staff only)
- Category system (via admin)
- Search by name, filter by category, available only toggle
- Session-based cart with stock validation (3 layers)
- Django Admin with list_display, search, filter, list_editable
- Forms with validation (price > 0, stock >= 0, quantity <= stock)
