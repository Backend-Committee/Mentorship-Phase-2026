# 📑 Adhkar System API
### Smart Reward & Gamification Engine

A comprehensive backend API for an Islamic *Adhkar* application built with Django REST Framework. This system goes beyond a simple text collection — it features a fully integrated **Gamification Engine** that motivates users by awarding points and automatically unlocking rewards based on daily consistency.

---

## 🚀 Key Features

**Advanced User Profiles** — Custom `AbstractUser` model that tracks total points, join date, and unlocked achievements alongside standard auth fields.

**Categorized Content** — Dhikr is organized into categories (Morning, Evening, Sleep) with full search and filter support via `SearchFilter`.

**Smart Reward Engine** — Uses Django `post_save` Signals to automatically check and unlock rewards in the background whenever a user earns points — zero blocking logic in the request cycle.

**Daily Progress Tracking** — Built-in validation prevents point farming by checking `completed_at__date` against today's date before allowing duplicate completions.

**Personalized Notifications** — Each user manages their own reminder times and can toggle notifications on/off independently.

**Admin Dashboard** — Role-based permissions (`IsAdminUser | IsAuthenticatedOrReadOnly`) give admins full CRUD while regular users get scoped read-only access.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Framework | Django & Django REST Framework (DRF) |
| Database | SQLite (default) |
| Authentication | Djoser + SimpleJWT (`Bearer` tokens, 1-day access / 7-day refresh) |
| Background Logic | Django Signals (`post_save`) |
| Media Storage | Django `MEDIA_ROOT` (reward images via `ImageField`) |

---

## 🏗 Project Architecture

The project is split into three focused Django apps:

```
AdhkarApp/
├── users/          # Auth, custom user model, rewards system
├── adhkar/         # Dhikr content library and categories
└── racking/        # Progress tracking and notifications
```

### Users App
Owns the custom `User` model (extends `AbstractUser`), the `Reward` catalog, and the `UserReward` join table that records when each reward was unlocked.

### Adhkar App
Manages the content library. A `Category` groups multiple `Adhkar` entries, each carrying a `points_value` that feeds into the reward engine.

### Tracking App (racking)
Handles all user interaction logic — recording `UserProgress`, preventing duplicate daily completions, firing the points signal, and managing per-user `Notification` settings.

---

## 🗄 Data Models

### `users` App

```python
# Custom user with points tracking
User(AbstractUser)
    email          → EmailField (unique)
    total_points   → IntegerField (default=0)
    created_at     → DateTimeField (auto)

# Reward catalog (admin-managed)
Reward
    title              → CharField
    description        → TextField
    points_threshold   → IntegerField   # points needed to unlock
    reward_type        → CharField
    image              → ImageField (upload_to='rewards_images/')

# Junction table — one row per unlocked reward
UserReward
    user        → FK(User)
    reward      → FK(Reward)
    unlocked_at → DateTimeField (auto)
    unique_together: (user, reward)     # no duplicates
```

### `adhkar` App

```python
Category
    name        → CharField
    description → TextField (optional)

Adhkar
    category      → FK(Category, related_name='adhkar_list')
    title         → CharField
    content       → TextField
    points_value  → IntegerField (default=1)
```

### `tracking` App

```python
UserProgress
    user          → FK(AUTH_USER_MODEL)
    adhkar        → FK(Adhkar)
    completed_at  → DateTimeField (auto)
    points_earned → IntegerField

Notification
    user          → FK(AUTH_USER_MODEL)
    is_enabled    → BooleanField (default=True)
    reminder_time → TimeField
```

---

## ⚡ Reward Signal — How It Works

```python
# racking/signals.py
@receiver(post_save, sender=UserProgress)
def update_user_system(sender, instance, created, **kwargs):
    if created:
        user = instance.user

        # 1. Add earned points to user's total
        user.total_points += instance.points_earned
        user.save()

        # 2. Find all rewards the user now qualifies for
        eligible = Reward.objects.filter(points_threshold__lte=user.total_points)

        # 3. Unlock only rewards not already granted
        for reward in eligible:
            if not UserReward.objects.filter(user=user, reward=reward).exists():
                UserReward.objects.create(user=user, reward=reward)
```

This keeps the reward logic **fully decoupled** from the API view layer — the endpoint just saves progress, and the signal handles everything else automatically.

---

## 🚦 API Endpoints

### 🔑 Authentication (`/auth/`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/users/` | Register a new user |
| `POST` | `/auth/jwt/create/` | Login — returns access & refresh tokens |
| `POST` | `/auth/jwt/refresh/` | Refresh an expired access token |
| `GET` | `/auth/users/me/` | Get the current user's profile |

### 📿 Content (`/adhkar/`)

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/adhkar/adhkar/` | List all Adhkar — supports `?search=` | Any authenticated |
| `POST` | `/adhkar/adhkar/` | Add a new Dhikr entry | Admin only |
| `GET` | `/adhkar/adhkar/<id>/` | Retrieve a single Dhikr | Any authenticated |
| `PUT/PATCH` | `/adhkar/adhkar/<id>/` | Edit a Dhikr entry | Admin only |
| `DELETE` | `/adhkar/adhkar/<id>/` | Delete a Dhikr entry | Admin only |

### 📊 Progress & Notifications (`/racking/`)

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `POST` | `/racking/userprogress/` | Record a Dhikr completion & earn points | Authenticated |
| `GET` | `/racking/notifications/` | List current user's notifications | Authenticated |
| `POST` | `/racking/notifications/` | Create a new reminder | Authenticated |
| `GET/PUT/DELETE` | `/racking/notifications/<id>/` | Manage a specific reminder | Owner only |

### 🏆 Rewards & Profile (`/users/`)

| Method | Endpoint | Description | Permission |
|---|---|---|---|
| `GET` | `/users/userprofile/` | View own profile and total points | Authenticated |
| `GET` | `/users/MyReward/` | List all rewards unlocked by current user | Authenticated |
| `GET` | `/users/reward/` | Browse the full reward catalog | Any authenticated |
| `POST` | `/users/reward/` | Create a new reward | Admin only |
| `PUT/DELETE` | `/users/reward/<id>/` | Edit or remove a reward | Admin only |

---

## 🛡 Permissions Logic

| Role | Access Level |
|---|---|
| **Unauthenticated** | Read-only on Adhkar and Categories |
| **Authenticated User** | Read content, record own progress, manage own notifications |
| **Staff / Admin** | Full CRUD on all content, rewards, and user data |

Ownership scoping is enforced in `get_queryset()` — users can only see and modify their own `UserProgress`, `Notification`, and `UserReward` records, even if they know another record's ID.

---

## ⚙️ Installation & Setup

**1. Clone the Repository**
```bash
git clone [your-repository-url]
cd AdhkarApp
```

**2. Create and Activate a Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Apply Migrations**
```bash
python manage.py migrate
```

**5. Create a Superuser** *(optional — needed to manage rewards and content)*
```bash
python manage.py createsuperuser
```

**6. Start the Development Server**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## 🔐 Authentication Flow

All protected endpoints require a `Bearer` token in the `Authorization` header:

```
Authorization: Bearer <your_access_token>
```

**Getting a token:**
```bash
POST /auth/jwt/create/
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access":  "eyJ...",   // valid for 1 day
  "refresh": "eyJ..."    // valid for 7 days
}
```

---

## 📝 Developer Notes

**Duplicate completion guard** — `RecordAdhkarProgressView` filters by `completed_at__date=timezone.now().date()` before saving. If a match exists, it raises a `ValidationError` with an Arabic-language message, keeping the UX localized.

**Decoupled reward system** — The signal in `racking/signals.py` is the only place that awards rewards. Views never touch `UserReward` directly, so the reward logic can be extended (e.g., adding badges, levels) without changing any endpoint.

**`unique_together` on `UserReward`** — Guarantees at the database level that no reward is granted twice, even under concurrent requests.

**Read-only serializer fields** — `points_earned` and `completed_at` are marked `read_only` on `UserProgressSerializer`, preventing users from manually inflating their score by submitting arbitrary values.

**Media files** — Reward images are served from `MEDIA_URL` in development. For production, replace `MEDIA_ROOT` with an object storage backend (e.g., S3).
