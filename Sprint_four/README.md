# CoffeeBlog

CoffeeBlog is a simple Django-based blog project that showcases a coffee-themed website with a home page, a blog listing page, and individual blog detail pages. The project uses sample data in the views layer rather than a database-backed blog model, making it a good starting point for learning Django routing, templates, and static files.

## Features

- Home page for the site
- Blog listing page with sample coffee-related posts
- Blog detail pages for individual posts
- Admin panel support via Django
- SQLite database by default
- Basic custom styling with static CSS

## Project Structure

- `CoffeeBlog/` - Django project root
  - `Blog/` - main app containing views, URLs, and templates
  - `CoffeeBlog/` - project settings and URL configuration
  - `templates/` - shared templates and page templates
  - `static/` - CSS and other static assets
  - `manage.py` - Django management entry point
- `db.sqlite3` - local SQLite database

## Tech Stack

- Python
- Django
- SQLite
- HTML/CSS

## Prerequisites

- Python 3.8 or newer
- Windows PowerShell (recommended for this project setup)

## Installation

1. Open a terminal in the project root (the folder that contains this README):

2. Activate the included virtual environment:
   ```powershell
   .\Scripts\Activate.ps1
   ```

   If PowerShell blocks script execution, run:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   ```

3. Install Django if needed in your environment:
   ```powershell
   pip install django
   ```

4. Apply the database migrations:
   ```powershell
   python .\CoffeeBlog\manage.py migrate
   ```

5. Create an admin user (optional but recommended):
   ```powershell
   python .\CoffeeBlog\manage.py createsuperuser
   ```

## Running the Project

Start the development server:

```powershell
python .\CoffeeBlog\manage.py runserver
```

Then open your browser at:

- `http://127.0.0.1:8000/` - home page
- `http://127.0.0.1:8000/home/` - home page alias
- `http://127.0.0.1:8000/blog_list/` - list of blog posts
- `http://127.0.0.1:8000/blog/1/` - detail page for a sample post
- `http://127.0.0.1:8000/admin/` - Django admin panel

## Current Data Model

This project currently uses hardcoded sample blog data inside `Blog/views.py`. There are no database models yet, so the blog content is not stored in a persistent model-based backend.

## Development Notes

To modify the content or add new pages:

- Update the sample blog data in `CoffeeBlog/Blog/views.py`
- Add or change URL patterns in `CoffeeBlog/Blog/urls.py`
- Edit templates in `CoffeeBlog/templates/`
- Update styling in `CoffeeBlog/static/css/style.css`

## Validation

The project was checked successfully with Django's system checks:

```powershell
python .\CoffeeBlog\manage.py check
```

## License

No license has been specified for this project yet.
