# Django Blog App

A simple blog application built with **Django**. Supports creating, editing, deleting, and viewing blog posts, along with a follow system similar to Instagram for authors.

---

## Features

- User authentication (login/register)
- Create, update, and delete blog posts
- Public/private posts support
- Follow/unfollow authors
- Instagram-style feed with:
  - Follow/unfollow buttons
  - Real-time button updates (AJAX)
- Comment system (optional)
- Responsive UI using **Bootstrap 5**

---

## Installation

1. **Clone the repository**

```bash
git clone <repository_url>
cd <project_folder>
```

2. **Create a virtual environment and activate it**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py migrate
```

5. **Create a superuser (optional)**

```bash
python manage.py createsuperuser
```

6. **Run the development server**

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## Usage

- **View Blog Feed:** Shows all public blog posts with author info and follow buttons.
- **Create Blog:** Logged-in users can create posts.
- **Edit Blog:** Edit your own posts.
- **Delete Blog:** Delete your own posts (with confirmation page or optional AJAX inline deletion).
- **Follow Authors:** Click “Follow” to follow an author; all posts by that author update automatically.
- **Comments:** Users can comment on posts (if enabled).

---

## Dependencies

- Django >= 4.2
- Bootstrap 5 (via CDN or static)
- Optional: Pillow (if using image uploads)

---

## Notes

- Make sure **CSRF tokens** are included for forms and AJAX requests.
- Follow/unfollow buttons use **AJAX** to avoid page reloads.
- Delete actions require **POST requests** to avoid 405 errors.
- For large feeds, `select_related` and `prefetch_related` are used to optimize queries.
