# 🏦 Bank System RESTful API

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-A30000?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)](https://jwt.io/)

A robust RESTful API for managing a banking system, featuring secure JWT authentication, automated card generation, and administrative controls.

---

## 🚀 Features

* **Secure Auth:** Registration, Login, and Logout with JWT Refresh/Access tokens.
* **Bank Management:** Full CRUD for banks (Admin only).
* **Account Operations:** Link users to banks with automated balance tracking.
* **Auto-Card Generation:** Creating an account automatically triggers credit/debit card creation.
* **Scalable Architecture:** Built using Django REST Framework best practices.

---

## 📍 API Reference

### 🔐 Authentication
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/authentication/register/` | Register a new user account |
| `POST` | `/api/authentication/token/` | Login & receive Access/Refresh tokens |
| `POST` | `/api/authentication/logout/` | Blacklist refresh token & logout |

### 🏛️ Bank Management
| Method | Endpoint | Access |
| :--- | :--- | :--- |
| `GET` | `/api/banks/` | All Users |
| `POST` | `/api/banks/` | Admin Only |
| `GET` | `/api/banks/{id}/` | All Users |
| `PUT/DELETE` | `/api/banks/{id}/` | Admin Only |

### 💳 Bank Accounts
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/banks/{id}/accounts/` | List all accounts in a specific bank |
| `POST` | `/api/banks/{id}/accounts/` | Create account (auto-generates card) |
| `GET` | `/api/{account_id}/` | View specific account details |
| `DELETE` | `/api/{account_id}/` | Remove account (Admin/Owner) |

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/bank-system-api.git](https://github.com/yourusername/bank-system-api.git)
   cd bank-system-api
   ```
2. **Set up Virtual Environment:**
    ```Bash

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**
    ```Bash
    pip install -r requirements.txt
    ```

4. **Run Migrations**:
    ```Bash
    python manage.py migrate
    ```

5. **Start Server**:
    ```Bash
    python manage.py runserver
    ```

## 🧪 Testing with Postman

1. Import the bank_api_collection.json file into Postman.

2. Set the baseUrl environment variable to http://127.0.0.1:8000/api.

3. Use the Login request to automatically populate your accessToken.
