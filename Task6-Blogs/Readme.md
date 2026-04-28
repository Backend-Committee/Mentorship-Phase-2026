# 📝 Secure Blog System — Django Week 6 Assignment

A fully functional blog application built with Django, featuring a complete authentication system, Class-Based Views, and strict permission controls.

---

## 🚀 Features

### 🔐 Authentication System

- **Register** — create a new account with username, email, and password
- **Login / Logout** — secure session-based authentication
- Custom styled forms with inline error messages
- Auto-login after successful registration

### 📰 Blog

- Browse all published posts on the home page
- View full post details with comments and view counter
- Browse posts by category
- Create, edit, and delete your own posts

### 🛡️ Permissions & Access Control

| Action           | Who can do it               |
| ---------------- | --------------------------- |
| View post list   | Anyone                      |
| View post detail | Anyone                      |
| Create a post    | Logged-in users only        |
| Edit a post      | Author only (403 otherwise) |
| Delete a post    | Author only (403 otherwise) |

---

## 🏗️ Project Structure

```
Task6-Blogs/
├── mainSite/               # Project settings & root URLs
│   ├── settings.py
│   └── urls.py
├── blog/                   # Blog app
│   ├── models.py           # BlogPost, Category, Comment
│   ├── views.py            # All CBVs
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   └── management/
│       └── commands/
│           └── load_data.py  # Seed command
├── accounts/               # Auth app
│   ├── views.py            # LoginView, LogoutView, RegisterView
│   ├── urls.py
│   └── forms.py            # RegisterUserForm
└── templates/
    ├── base.html
    ├── home.html
    ├── blog_list.html
    ├── blog_detail.html
    ├── blog_form.html
    ├── blog_confirm_delete.html
    ├── category_list.html
    ├── category_posts.html
    ├── login.html
    └── register.html
```

---

## 🧠 Key Concepts Used

### Class-Based Views (CBVs)

All views are written as CBVs — no function-based views in the blog app.

| View         | Purpose                        |
| ------------ | ------------------------------ |
| `ListView`   | Display all posts / categories |
| `DetailView` | Display a single post          |
| `CreateView` | Form to write a new post       |
| `UpdateView` | Form to edit an existing post  |
| `DeleteView` | Confirm and delete a post      |

### Mixins

```python
# Only logged-in users can create posts
class PostCreateView(LoginRequiredMixin, CreateView):
    ...

# Only the author can edit or delete
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user == self.get_object().author
```

- `LoginRequiredMixin` — redirects unauthenticated users to login
- `UserPassesTestMixin` — runs `test_func()` and returns **403 Forbidden** if it fails

### Models

```python
class BlogPost(models.Model):
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True)
    author       = models.ForeignKey(User, on_delete=models.CASCADE)  # linked to auth user
    content      = models.TextField()
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_date = models.DateField()
    is_published = models.BooleanField(default=True)
    views_count  = models.IntegerField(default=0)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repo & create virtual environment

```bash
git clone <repo-url>
cd Task6-Blogs
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 2. Install dependencies

```bash
pip install django
```

### 3. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Load sample data

```bash
python manage.py load_data
```

This creates 4 categories, 8 blog posts, 7 comments, and 8 user accounts.
All sample users have the password: `pass1234!`

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Run the server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/**

---

## 🗺️ URL Map

| URL                    | View                | Access         |
| ---------------------- | ------------------- | -------------- |
| `/`                    | Home — latest posts | Public         |
| `/blog/`               | All posts           | Public         |
| `/blog/<slug>/`        | Post detail         | Public         |
| `/blog/new/`           | Create post         | Login required |
| `/blog/<slug>/update/` | Edit post           | Author only    |
| `/blog/<slug>/delete/` | Delete post         | Author only    |
| `/category/`           | Category list       | Public         |
| `/category/<slug>/`    | Posts by category   | Public         |
| `/accounts/login/`     | Login               | Public         |
| `/accounts/register/`  | Register            | Public         |
| `/accounts/logout/`    | Logout (POST only)  | Login required |
| `/admin/`              | Django admin        | Superuser      |

---

## 🔒 Security Notes

- Logout is **POST only** — prevents CSRF attacks via malicious links
- All forms include `{% csrf_token %}` — protects against cross-site request forgery
- Ownership is enforced server-side — users cannot edit others' posts even by manipulating URLs
- Passwords are hashed by Django's auth system — never stored in plain text

---

## 🛠️ Admin Panel

Visit `/admin/` with a superuser account to manage posts, categories, and comments directly.

Registered models:

- `BlogPost` — with filters by published status, date, and category
- `Category` — with search by name

---

_Built with Django 6.0 · Star Union Backend Committee · Task 6_
