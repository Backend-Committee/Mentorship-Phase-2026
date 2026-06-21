**☽  Adhkar App**

REST API Documentation

*Built with Django REST Framework  •  JWT Authentication  •  Modular Architecture*

| **Python** | **Django** | **DRF** | **JWT** | **Djoser** | **SQLite** |
| --- | --- | --- | --- | --- | --- |

# **📋  Project Overview**

Adhkar App is a Django REST Framework API designed to help users maintain daily adhkar habits. The system supports full lifecycle management — from browsing and recording adhkar to earning points and unlocking rewards.

## **✨  Key Features**

- Browse adhkar by category (Morning, Evening, Sleep, Prayer)

- Record completed adhkar with automatic duplicate prevention

- Earn points for consistency and unlock achievement rewards

- Automated reward system powered by Django signals

- Notification reminders with per-user scheduling

- Secure JWT-based authentication via Djoser

## **🏗️  Architecture**

The project follows a clean, modular architecture divided into 3 Django apps:

| **App** | **Responsibility** | **Key Models** |
| --- | --- | --- |
| **users** | User accounts, rewards, profile management | User, Reward, UserReward |
| **adhkar** | Adhkar content and category management | Category, Adhkar |
| **racking** | Progress tracking, points, notifications | UserProgress, Notification |

# **👤  App 1: Users**

Manages user accounts, achievement rewards, profile data, and tracks which rewards each user has unlocked.

## **📦  Models**

### **User**

| **Field** | **Type** | **Description** |
| --- | --- | --- |
| **username** | CharField | Unique username for login |
| **email** | EmailField | User email address |
| **password** | CharField | Hashed password (Django default) |
| **total_points** | IntegerField | Accumulated points from adhkar |
| **created_at** | DateTimeField | Account creation timestamp |

### **Reward**

| **Field** | **Type** | **Description** |
| --- | --- | --- |
| **title** | CharField | Badge or reward name (e.g., Bronze Badge) |
| **description** | TextField | What the reward represents |
| **points_threshold** | IntegerField | Points needed to unlock (e.g., 20, 50) |
| **reward_type** | CharField | Type/category of reward |
| **image** | ImageField | Badge image file |

| 🏅  Example Rewards:    Bronze Badge → 20 pts   │   Silver Badge → 50 pts   │   Gold Badge → 100 pts |
| --- |

### **UserReward**

| **Field** | **Type** | **Description** |
| --- | --- | --- |
| **user** | ForeignKey | Reference to the User model |
| **reward** | ForeignKey | Reference to the Reward model |
| **unlocked_at** | DateTimeField | Timestamp when reward was earned |

| 🔒  Constraint: A user cannot unlock the same reward twice (unique_together constraint) |
| --- |

## **🌐  API Endpoints**

### **Rewards**

| **Method** | **Endpoint** | **Access** | **Description** |
| --- | --- | --- | --- |
| **GET** | /users/reward/ | Public | List all rewards |
| **POST** | /users/reward/ | Admin only | Create a new reward |
| **GET** | /users/reward/<id>/ | Public | Retrieve reward detail |
| **PUT/PATCH** | /users/reward/<id>/ | Admin only | Update reward |
| **DELETE** | /users/reward/<id>/ | Admin only | Delete reward |

### **User Profile**

| **Method** | **Endpoint** | **Access** | **Description** |
| --- | --- | --- | --- |
| **GET** | /users/userprofile/ | Authenticated | Get current user profile |

Response example:

{ "username": "habiba", "email": "habiba@gmail.com", "total_points": 75, "is_staff": false }

### **My Rewards**

| **Method** | **Endpoint** | **Access** | **Description** |
| --- | --- | --- | --- |
| **GET** | /users/MyReward/ | Authenticated | List user's unlocked rewards only |

# **📿  App 2: Adhkar**

Manages all adhkar content and their categories. Supports public browsing and search while restricting write operations to admin users.

## **📦  Models**

### **Category**

| **Field** | **Type** | **Description** |
| --- | --- | --- |
| **name** | CharField | Category name (e.g., Morning, Evening) |
| **description** | TextField | Category description and purpose |

Built-in categories: Morning  •  Evening  •  Sleep  •  Prayer

### **Adhkar**

| **Field** | **Type** | **Description** |
| --- | --- | --- |
| **category** | ForeignKey | Category this adhkar belongs to |
| **title** | CharField | Name of the adhkar (e.g., Ayat Al Kursi) |
| **content** | TextField | Full Arabic text and translation |
| **points_value** | IntegerField | Points awarded for completing this adhkar |

## **🌐  API Endpoints**

### **Adhkar**

| **Method** | **Endpoint** | **Access** | **Description** |
| --- | --- | --- | --- |
| **GET** | /adhkar/adhkar/ | Public | List all adhkar (supports search) |
| **POST** | /adhkar/adhkar/ | Admin only | Create new adhkar |
| **GET** | /adhkar/adhkar/<id>/ | Public | Retrieve single adhkar |
| **PUT/PATCH** | /adhkar/adhkar/<id>/ | Admin only | Update adhkar |
| **DELETE** | /adhkar/adhkar/<id>/ | Admin only | Delete adhkar |

| 🔍  Search Support: Filter by title or category name using ?search=morning |
| --- |

### **Categories**

| **Method** | **Endpoint** | **Access** | **Description** |
| --- | --- | --- | --- |
| **GET** | /adhkar/category/ | Public | List all categories |
| **POST** | /adhkar/category/ | Admin only | Create new category |
| **GET** | /adhkar/category/<id>/ | Public | Retrieve category detail |
| **PUT/PATCH** | /adhkar/category/<id>/ | Admin only | Update category |
| **DELETE** | /adhkar/category/<id>/ | Admin only | Delete category |

## **🔐  Permission System**

A custom ReadOnlyOrAdmin permission class controls access:

| **User Type** | **Allowed Methods** |
| --- | --- |
| Public / Unauthenticated | GET  •  HEAD  •  OPTIONS  (safe methods only) |
| Admin (is_staff=True) | GET  •  POST  •  PUT  •  PATCH  •  DELETE  (all methods) |

if request.method in SAFE_METHODS:
    return True
return request.user.is_authenticated and request.user.is_staff

# **📊  App 3: Racking (Progress Tracking)**

The core engine of the app — handles user progress, automatic point accumulation, signal-driven reward unlocking, and personal notification management.

## **📦  Models**

### **UserProgress**

| **Field** | **Type** | **Description** |
| --- | --- | --- |
| **user** | ForeignKey | The user completing the adhkar |
| **adhkar** | ForeignKey | The adhkar being completed |
| **completed_at** | DateTimeField | Timestamp of completion (auto-set) |
| **points_earned** | IntegerField | Points copied from adhkar at completion time |

| 🚫  Duplicate Prevention: A user cannot complete the same adhkar twice in the same calendar day. |
| --- |

### **Notification**

| **Field** | **Type** | **Description** |
| --- | --- | --- |
| **user** | ForeignKey | Owner of this notification setting |
| **is_enabled** | BooleanField | Whether the reminder is active |
| **reminder_time** | TimeField | Time of day to send the reminder |

## **🌐  API Endpoints**

### **Progress Tracking**

| **Method** | **Endpoint** | **Access** | **Description** |
| --- | --- | --- | --- |
| **POST** | /racking/userprogress/ | Authenticated | Record a completed adhkar |

Request body:

{ "adhkar": 1 }

The system automatically:

- Checks for duplicate completion today

- Reads the adhkar's point value

- Saves progress and updates user's total_points

- Triggers signal to check and unlock rewards

### **Notifications**

| **Method** | **Endpoint** | **Access** | **Description** |
| --- | --- | --- | --- |
| **GET** | /racking/notifications/ | Authenticated | List user's notifications |
| **POST** | /racking/notifications/ | Authenticated | Create notification reminder |
| **GET** | /racking/notifications/<id>/ | Owner only | View specific notification |
| **PUT/PATCH** | /racking/notifications/<id>/ | Owner only | Update reminder settings |
| **DELETE** | /racking/notifications/<id>/ | Owner only | Delete reminder |

| 🔒  Security: Each user can only access and modify their own notifications. Filtered by request.user automatically. |
| --- |

## **⚡  Signals Logic**

Django signals decouple the reward logic from views, keeping the codebase clean and maintainable.

Signal: post_save on UserProgress — fires only when a new record is created:

# Step 1: Add points to user
user.total_points += instance.points_earned
user.save()

# Step 2: Find all qualifying rewards
rewards = Reward.objects.filter(points_threshold__lte=user.total_points)

# Step 3: Unlock any not yet awarded
for reward in rewards:
    UserReward.objects.get_or_create(user=user, reward=reward)

| **✅  Benefits of Signals** Clean, focused view logic Business logic is separated Easier to test independently Better long-term maintainability | **🔄  Signal Flow** UserProgress saved post_save signal fires Points added to user Rewards checked & unlocked |
| --- | --- |

# **🔑  Authentication**

Authentication is handled via Djoser + JWT (JSON Web Tokens), providing stateless, secure API access with standard register/login/refresh flows.

## **Endpoints**

### **Register**

| **Method** | **Endpoint** | **Access** | **Description** |
| --- | --- | --- | --- |
| **POST** | /auth/users/ | Public | Register a new user account |

{
  "username": "habiba",
  "email": "habiba@gmail.com",
  "password": "12345678",
  "re_password": "12345678"
}

### **Login**

| **Method** | **Endpoint** | **Access** | **Description** |
| --- | --- | --- | --- |
| **POST** | /auth/jwt/create/ | Public | Authenticate and receive JWT tokens |

Response:

{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}

### **Refresh Token**

| **Method** | **Endpoint** | **Access** | **Description** |
| --- | --- | --- | --- |
| **POST** | /auth/jwt/refresh/ | Public | Exchange refresh token for new access token |

{ "refresh": "<refresh_token>" }

### **Logout**

| ℹ️  JWT is stateless — logout is handled client-side by deleting both tokens from storage.  localStorage.removeItem('access') localStorage.removeItem('refresh') |
| --- |

# **🔄  Full Application Workflow**

## **Admin Workflow**

- Create categories (Morning, Evening, Sleep, Prayer)

- Add adhkar content with point values

- Define achievement rewards with point thresholds

- Manage and moderate all content

## **User Workflow**

- Register a new account  →  POST /auth/users/

- Login and receive JWT tokens  →  POST /auth/jwt/create/

- Browse and search adhkar  →  GET /adhkar/adhkar/?search=morning

- Complete an adhkar  →  POST /racking/userprogress/

- System saves progress and adds points automatically

- Signal checks and unlocks eligible rewards

- View earned rewards  →  GET /users/MyReward/

- Set notification reminders  →  POST /racking/notifications/

# **🛠️  Tech Stack**

| **Technology** | **Version** | **Purpose** |
| --- | --- | --- |
| **Python** | 3.10+ | Core programming language |
| **Django** | 4.x | Web framework |
| **Django REST Framework** | 3.x | API development toolkit |
| **Djoser** | Latest | Authentication endpoints & user management |
| **Simple JWT** | Latest | JSON Web Token authentication |
| **SQLite** | Built-in | Database (development) |

*Adhkar App API  •  Built with Django REST Framework  •  JWT Secured*
```mermaid
erDiagram
    USER ||--o{ USERPROGRESS : tracks
    USER ||--o{ USERREWARD : unlocks
    USER ||--o{ NOTIFICATION : has
    REWARD ||--o{ USERREWARD : unlocked_by
    ADHKAR ||--o{ USERPROGRESS : tracked_by
    CATEGORY ||--o{ ADHKAR : contains

    USER {
        int user_id PK
        string name
        string email
        string Password
        int total_points
        datetime created_at
    }

    REWARD {
        int reward_id PK
        string title
        string description
        int points_threshold
        string reward_type
    }

    USERREWARD {
        int user_reward_id PK
        int user_id FK
        int reward_id FK
        datetime unlocked_at
    }

    USERPROGRESS {
        int user_progress_id PK
        int user_id FK
        int adhkar_id FK
        datetime completed_at
        int points_earned
    }

    ADHKAR {
        int adhkar_id PK
        int category_id FK
        string title
        string content
        int points_value
    }

    CATEGORY {
        int category_id PK
        string name
        string description
    }

    NOTIFICATION {
        int notification_id PK
        int user_id FK
        boolean is_enabled
        time reminder_time
    }
Link ERD { https://lucid.app/lucidchart/c4cd0041-0f49-43a6-83b7-5523d51749c9/edit?viewport_loc=-578%2C-2251%2C2383%2C2026%2C0_0&invitationId=inv_989f7311-6bb5-401e-9ee6-ba577bd7de44 }
```
