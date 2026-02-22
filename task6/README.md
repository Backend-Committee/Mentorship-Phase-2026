# AuthSystem — Django Blog & Authentication

A full-stack Django web application with a complete user authentication system and a blog platform with role-based access control using Django's built-in mixins.



## 📁 Project Structure

```
AuthSystem/
├── .venv/                            # Virtual environment
├── README.md
└── Auth/                             # Django project root
    ├── manage.py
    ├── db.sqlite3                    # SQLite database
    │
    ├── Auth/                         # Project config
    │   ├── settings.py
    │   ├── urls.py                   # Root URL configuration
    │   ├── wsgi.py
    │   └── asgi.py
    │
    ├── member/                       # Authentication app
    │   ├── views.py                  # login, logout, register, home
    │   ├── urls.py
    │   ├── models.py
    │   └── migrations/
    │
    ├── blog/                         # Blog app
    │   ├── views.py                  # Class-based views with mixins
    │   ├── urls.py
    │   ├── models.py                 # Post model
    │   └── migrations/
    │
    └── templates/
        ├── parts/
        │   └── navbar.html           # Shared navbar (included in all pages)
        ├── auth/
        │   ├── login.html
        │   ├── register.html
        │   └── home.html
        └── blog/
            ├── post_list.html
            ├── post_detail.html
            ├── post_form.html        # Shared for create & update
            └── post_confirm_delete.html
```

---

## 🔐 Authentication (member app)

Built using Django's built-in `authenticate`, `login`, and `logout` from `django.contrib.auth`.

### Features
- **Register** — creates a new user using `UserCreationForm`, then auto-logs them in
- **Login** — authenticates with username & password, shows error messages on failure
- **Logout** — POST-only request (CSRF protected) to prevent accidental logouts
- **Flash messages** — success/error feedback on every action

### Member URLs

| URL               | Name | Description |
|-------------------|------|---------|
| `/`               | `home` | Home page (welcome screen) |
| `/login_user/`    | `login_user` | Login form |
| `/logout_user/`   | `logout_user` | Logout  |
| `/register_user/` | `register_user` | Registration form |

---

## 📝 Blog (blog app)

A full CRUD blog system built with Django **class-based views (CBVs)**.

### Post Model

| Field | Type | Description |
|-------|------|-------------|
| `title` | `CharField(200)` | Title of the post |
| `content` | `TextField` | Body content |
| `author` | `ForeignKey(User)` | Linked to Django's built-in User |
| `created_at` | `DateTimeField` | Auto-set on creation |

### Blog URLs

| URL | Name | View | Access |
|-----|------|------|--------|
| `/blog/` | `blog-home` | `PostListView` | Public |
| `/blog/post/<id>/` | `post-detail` | `PostDetailView` | Public |
| `/blog/post/new/` | `post-create` | `PostCreateView` | Login required |
| `/blog/post/<id>/update/` | `post-update` | `PostUpdateView` | Author only |
| `/blog/post/<id>/delete/` | `post-delete` | `PostDeleteView` | Author only |

---

## 🧩 Mixins Used

Django mixins are classes you add to a class-based view to inject extra behavior without rewriting logic.

### `LoginRequiredMixin`
> From `django.contrib.auth.mixins`

Redirects unauthenticated users to the login page if they try to access a protected view.

Used on:
- `PostCreateView` — only logged-in users can write a post
- `PostUpdateView` — only logged-in users can reach the edit form
- `PostDeleteView` — only logged-in users can reach the delete form

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

---

### `UserPassesTestMixin`
> From `django.contrib.auth.mixins`

Calls a `test_func()` method on the view. If it returns `False`, the user gets a **403 Forbidden** response automatically.

Used on:
- `PostUpdateView` — only the post's author can edit it
- `PostDeleteView` — only the post's author can delete it

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
```

---

## 🔒 Access Control Summary

| Action | Who Can Do It |
|--------|--------------|
| View post list | Anyone (public) |
| View post detail | Anyone (public) |
| Create a post | Logged-in users only |
| Edit a post | The post's author only (403 for others) |
| Delete a post | The post's author only (403 for others) |
| Logout | POST request only (CSRF protected) |

---

## 🧭 Navbar

All pages share a single navbar via `{% include 'parts/navbar.html' %}`.

| State | Links Shown |
|-------|------------|
| Guest (not logged in) | Home, Blog, Login, Register |
| Logged in | Home, Blog, Logout (red button) |

