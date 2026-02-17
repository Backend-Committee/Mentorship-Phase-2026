# 📖 Static Django Blog

A simple Django blog using static data instead of a database. Perfect for learning, prototyping, or building a small portfolio project.

# ⚡ Features

Display a list of blog posts

View detailed content for each blog post

Static data stored in Python dictionaries (no database required)

## Blog posts include:

- Title

- Author

- Date

- Content

- Tags

Clean and responsive templates with base layout

URL-friendly slugs for each post

Easy to extend with more posts or features

## 🗂 Project Structure
```text
project_root/
│
├── post/                     # Django app
│   ├── templates/
│   │   └── post/
│   │       ├── base.html
│   │       ├── index.html
│   │       └── post.html
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── project_name/
│   └── settings.py
│
├── manage.py
└── README.md
```

# 🔗 Endpoints / URLs
## Endpoint	HTTP Method	Description
/	GET	List all blog posts (index page)
/<slug:slug>/	GET	View details of a single blog post

> Example: /first-post/	GET	Displays "My First Blog Post" content
# 🛠 Installation

## Clone the repository:
```bash
git clone https://github.com/your-username/static-django-blog.git
cd static-django-blog

# Create and activate a virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate


# Install Django:

pip install django


Run the development server:

python manage.py runserver

```
## Open in browser:
```bash
http://127.0.0.1:8000/
```

# 📝 Usage

To add a new blog post, update BLOG_POSTS in views.py:
```py
BLOG_POSTS.append({
    "id": 21,
    "slug": "new-post",
    "title": "My New Blog Post",
    "author": "Your Name",
    "date": "2026-02-17",
    "content": "This is the content of my new post.",
    "tags": ["django", "python"],
})
```

Posts automatically appear on the index page.

# 🎨 Templates

- base.html – Base layout with header, footer, and container

- index.html – Displays all blog posts in a list

- post.html – Shows single post details with tags and author info

# 🔍 Features to Add (Optional)

Pagination for long lists of posts

Tag filtering or category pages

Search functionality

Dark/light mode

Comments section (static or dynamic)

Deploy to a cloud server (Heroku, Render, etc.)

# 👨‍💻 Author

Your Name – Your Contact / GitHub Profile
