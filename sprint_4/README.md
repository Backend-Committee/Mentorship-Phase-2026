# 📝 Mini Blog App - Django

A simple and elegant Blog Web Application built with Python and Django. This project is developed as part of **Task 4 (Sprint 4)** for the **Mentorship Phase 2026**.

## ✨ Features
* **Home Page:** A welcoming landing page for the application.
* **Blog List:** Displays a collection of all available blog posts with their titles and summaries.
* **Blog Details:** Dynamic routing to view the full content of a specific blog post based on its unique ID.
* **Custom UI:** Styled with custom CSS for a modern, dark-themed user interface.
* **Mock Database:** Uses a structured Python list of dictionaries to simulate database fetching for fast development and testing.

## 🛠️ Technologies Used
* **Backend:** Python 3, Django 5.x
* **Frontend:** HTML5, CSS3 (Custom Static Files)
* **Version Control:** Git & GitHub

## 🚀 How to Run the Project Locally

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

pip install django
python manage.py runserver


## 📂 Project Structure
```text
Mini_Blog_app/
│
├── Mini_Blog_app/       # Core Django project settings
├── blog_pages/          # Main app containing views, urls, and mock data
├── static/              # CSS, images, and other static assets
├── templates/           # HTML templates (home, blog_list, blog_details)
├── manage.py            # Django project manager
└── .gitignore           # Git ignore rules for venv and cache

