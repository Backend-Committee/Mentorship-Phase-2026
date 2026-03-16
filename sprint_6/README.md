# Secure Blog System (S_Blog_sys) 📝

## About the Project
A simple and easy-to-use blog system built with **Django**. This project allows users to create accounts, write posts, and easily edit or delete their own content.

## Key Features ✨
* **Authentication System:** Includes Login, Logout, and Sign Up functionalities.
* **Post Management (CRUD Operations):**
  * View a list of all published posts (List).
  * Read the full details of individual posts (Detail).
  * Create new posts (restricted to logged-in users).
  * Update and delete posts (restricted to the original author to ensure privacy).
* **Security & Permissions:** Utilizes `LoginRequiredMixin` and `UserPassesTestMixin` to ensure users cannot access unauthorized pages or perform actions they aren't permitted to.

## Tech Stack 🛠️
* **Language:** Python
* **Framework:** Django 5.2
* **Database:** SQLite3 (Default)
* **Architecture:** Built entirely using Class-Based Views (CBVs) for clean and maintainable code.

## Project Directory Structure 📂

Here is a visual overview of the project's structure:

```text
S_Blog_sys/
├── .venv/                   # Virtual environment (ignored in git)
├── blogs/                   # App handling all blog post logic (CRUD)
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── ...
├── pages/                   # App handling static or general public pages
├── S_Blog_sys/              # Main Django project configuration folder
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/                  # Static files (CSS, JavaScript, Images)
├── templates/               # Global folder for HTML templates
│   ├── blogs/               # Templates for posts (List, Detail, Create, etc.)
│   └── users/               # Templates for auth (Login, Signup, etc.)
├── users/                   # App handling user authentication and accounts
│   ├── models.py
│   ├── views.py
│   └── ...
├── db.sqlite3               # Default SQLite database
├── manage.py                # Django management script
└── requirements.txt         # List of project dependencies