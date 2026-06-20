# miniAmazon (Amazon Backend)

A lightweight e-commerce backend built with Django. This project implements core features for a minimal Amazon-like store: products, cart, orders, and admin management.

## Features
- Product listing and details
- Shopping cart management
- Order creation and history
- Django admin for managing products and orders
- SQLite database for easy local development

## Tech stack
- Python 3.8+
- Django (check requirements.txt)
- SQLite (default development DB)

## Quickstart (Windows)
1. Clone the repo:
   git clone <repo-url>
2. Create and activate a virtual environment:
   python -m venv venv
   venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
   (If requirements.txt is missing, install Django: pip install django)
4. Apply migrations:
   python manage.py migrate
5. (Optional) Create a superuser for admin:
   python manage.py createsuperuser
6. Run the development server:
   python manage.py runserver
7. Open http://127.0.0.1:8000/ in your browser.

## Configuration
- SECRET_KEY, DEBUG and other sensitive settings may be configured in `Amazon/settings.py` or via environment variables. For production, ensure DEBUG=False and use a secure SECRET_KEY.
- Database: By default the project uses `db.sqlite3`. To switch databases, update `DATABASES` in settings.

## API & Routes
This project uses Django views and URL routing. Key app folders include:
- `main/` — site homepage and product listing
- `cart/` — cart management
- `order/` — order creation and history
- `Amazon/` — project settings and URLs

Check `Amazon/urls.py` and each app's `urls.py` for available endpoints. Example endpoints (may vary):
- `/` — homepage / product list
- `/cart/` — view cart
- `/order/checkout/` — create an order
- `/admin/` — Django admin

## Database
A `db.sqlite3` file is included for convenience. To reset the DB locally:
- Delete `db.sqlite3` and run `python manage.py migrate`.

## Tests
Run Django tests with:
```
python manage.py test
```

## Static files & Templates
- Templates are in `templates/`.
- Static files are in `static/`. Use `collectstatic` for production static collection.

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Open a pull request describing your changes

Be concise in PR descriptions and ensure existing tests pass.

## Troubleshooting
- If migrations fail, ensure the virtualenv is active and dependencies installed.
- If port 8000 is busy, run `python manage.py runserver 8080`.

## License
Specify your project license here.


If you want, a more detailed README can be generated listing exact endpoints and setup steps after inspecting specific files (settings, urls, and requirements).