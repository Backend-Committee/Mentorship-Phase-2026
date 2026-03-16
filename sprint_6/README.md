# Simple Blog System (S_Blog_sys) 📝

## About the Project
A simple, robust, and easy-to-use blog system built with **Django 5.2**. This project allows users to create accounts, write posts, and manage their own content. It is designed following best practices using Django's Class-Based Views (CBVs) to keep the code clean and maintainable.

## Key Features ✨
* **User Authentication:** Fully functional Login, Logout, and Sign-Up systems.
* **Complete CRUD Operations:** Users can **C**reate, **R**ead, **U**pdate, and **D**elete their blog posts.
* **Privacy & Security:** Users can only edit or delete posts that they authored. Guest users cannot create posts without logging in.
* **Clean UI Structure:** Global templates folder used to manage the HTML pages for both the blog and user authentication.

## Tech Stack 🛠️
* **Language:** Python 3
* **Framework:** Django 5.2.11
* **Database:** SQLite3 (Default, easily scalable to PostgreSQL)
* **Architecture:** Class-Based Views (CBVs) and Model-View-Template (MVT) pattern.

---

## How It Works (Under the Hood) 🔍

Here is a detailed breakdown of how the project operates based on its code:

### 1. Database Models (`models.py`)
The database relies on two main components:
* **The `User` Model:** Django's built-in authentication model is used to handle user accounts securely.
* **The `Post` Model:** This is the core of the blog app. Each post contains:
  * `title`: The title of the post (max 100 characters).
  * `content`: The main text body of the post.
  * `date_posted`: Automatically records the exact time the post was created (`auto_now_add=True`).
  * `user`: A foreign key linking the post to its author (the `User` model). If a user is deleted, their posts are also deleted (`CASCADE`).

### 2. Views (Class-Based Views)
The project relies entirely on CBVs to handle web requests efficiently:
* **Blog Views (`blogs/views.py`):**
  * `PostListView`: Fetches all blog posts from the database and displays them on the home page.
  * `PostDetailView`: Shows the full details of a specific post.
  * `PostCreateView`: Renders a form to create a new post and automatically assigns the logged-in user as the author.
  * `PostUpdateView` & `PostDeleteView`: Handle editing and removing posts.
* **User Views (`users/views.py`):**
  * `UserLogin` & `UserLogout`: Extend Django's built-in auth views to handle sessions.
  * `UserSignup`: Uses Django's `UserCreationForm` to register new users and automatically logs them in upon successful registration.

### 3. Security & Permissions (Mixins)
To protect the routes, the project uses Django Mixins:
* `LoginRequiredMixin`: Applied to Create, Update, and Delete views. It kicks unauthenticated users to the login page if they try to access these URLs.
* `UserPassesTestMixin`: A custom test function applied to Update and Delete views. It checks if `self.request.user == post.user`. This ensures that even if a user is logged in, they absolutely cannot edit or delete a post written by someone else.

---

## Project Directory Structure 📂

```text
S_Blog_sys/
├── .venv/                   # Virtual environment (ignored in git)
├── blogs/                   # App handling all blog post logic (CRUD)
│   ├── models.py            # Contains the Post database table
│   ├── views.py             # Contains the CBVs for listing, creating, etc.
│   └── urls.py
├── pages/                   # App handling static or general public pages
├── S_Blog_sys/              # Main Django project configuration folder
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/                  # Static files (CSS, JavaScript, Images)
├── templates/               # Global folder for HTML templates
│   ├── blogs/               # Templates for posts (List.html, Detail.html, etc.)
│   └── users/               # Templates for auth (Login.html, Signup.html, etc.)
├── users/                   # App handling user authentication and accounts
│   └── views.py             # Login, Logout, and Signup views
├── db.sqlite3               # Default SQLite database
├── manage.py                # Django management script
└── requirements.txt         # List of project dependencies