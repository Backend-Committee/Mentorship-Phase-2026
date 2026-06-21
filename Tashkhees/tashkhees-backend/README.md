# Tashkhees Backend

A Django REST API for a medical/laboratory management system. This backend provides user management with role-based profiles (patients, doctors, lab admins), facility management (clinics and laboratories), and a secure file upload system with an approval workflow.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Apps](#apps)
  - [Users](#users)
  - [Files](#files)
  - [Facilities](#facilities)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [File Upload & Approval Workflow](#file-upload--approval-workflow)
- [Testing with Resty](#testing-with-resty)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)

---

## Overview

Tashkhees is a medical information system backend built with **Django 6.0** and **Django REST Framework**. It features:

- **Custom User Model** with email-based authentication
- **Role-based Profiles**: Patient, Doctor, Lab Admin
- **JWT Authentication** via `djangorestframework-simplejwt`
- **File Upload System** with sender/receiver tracking and approval workflow
- **Facility Management** for Clinics and Laboratories
- **Resty Client** integration for API testing

---

## Project Structure

```
tashkhees-backend/
├── project/
│   ├── project/              # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── users/                # User management app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── managers.py
│   │   └── admin.py
│   ├── files/                # File upload & approval app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── facilities/           # Facility management app
│   │   ├── models.py
│   │   ├── views.py
│   │   └── admin.py
│   ├── manage.py
│   └── db.sqlite3
├── resty/                    # Resty client test files
│   ├── auth.resty
│   ├── users.resty
│   └── files.resty
├── .venv/                    # Virtual environment
├── pyrightconfig.json
└── README.md
```

---

## Apps

### Users

The `users` app provides a custom user model and role-based profiles.

#### Models

| Model | Description |
|-------|-------------|
| `User` | Custom user with email as unique identifier |
| `Patient` | Patient profile linked to User (medical history) |
| `Doctor` | Doctor profile linked to User (specialization) |
| `LabAdmin` | Lab Admin profile linked to User |

#### User Model Fields

- `id` — Auto-increment primary key
- `username` — User display name
- `email` — Unique email address (used for login)
- `is_staff` — Admin/staff status
- `is_active` — Account active status
- `date_joined` — Account creation timestamp

#### Profile Relationships

All profiles use a **OneToOneField** linking to `User`:
- `Patient.user` → `user.patient_profile`
- `Doctor.user` → `user.doctor_profile`
- `LabAdmin.user` → `user.lab_admin_profile`

---

### Files

The `files` app handles file uploads with a sender/receiver approval workflow.

#### Models

| Model | Description |
|-------|-------------|
| `File` | Stores the actual uploaded file |
| `UploadFile` | Tracks file transfer between users with approval status |

#### UploadFile Model Fields

- `file` — ForeignKey to `File`
- `uploader` — ForeignKey to `User` (sender)
- `receiver` — ForeignKey to `User` (recipient)
- `approved` — Boolean, default `False`
- `uploaded_at` — Timestamp

#### Approval Workflow

1. **Uploader** sends a file to a **Receiver** via `POST /api/upload/`
2. **Receiver** views unapproved files via `GET /api/upload/unapproved/`
3. **Receiver** approves the file via `POST /api/upload/<id>/approve/`
4. **Receiver** views approved files via `GET /api/upload/approved/`

> **Security**: Only the receiver can approve a file. Attempting to approve as another user returns `403 Forbidden`.

---

### Facilities

The `facilities` app manages medical facilities. `Facility` is an **abstract base model** — you cannot create a standalone `Facility`. Instead, you create concrete instances as either a `Clinic` or a `Laboratory`.

#### Models

| Model | Description |
|-------|-------------|
| `Facility` | **Abstract** base model (name, description, hours, contact info) |
| `Clinic` | Concrete facility with specialty, consultation fee, doctors |
| `Laboratory` | Concrete facility with home sample collection, online results |
| `Address` | Address information linked to any facility via generic relation |

#### Facility (Abstract) Fields

- `name` — Facility name
- `description` — Description
- `phone` — Contact phone
- `email` — Contact email
- `website` — Website URL
- `opening_time` / `closing_time` — Operating hours
- `is_active` — Active status

> **Note:** Since `Facility` is abstract, it has no database table and no API endpoints. Use `/api/facilities/clinics/` or `/api/facilities/laboratories/` instead.

---

## Authentication

The API uses **JWT (JSON Web Token)** authentication via `djangorestframework-simplejwt`.

### Token Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/token/` | Obtain access & refresh tokens |
| `POST` | `/api/token/refresh/` | Refresh access token |

### Token Request Body

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### Token Response

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Using Tokens

Include the access token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

---

## API Endpoints

### Users

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| `POST` | `/api/users/register/` | AllowAny | Register a new user |
| `GET` | `/api/users/` | IsAdminUser | List all users |
| `GET` | `/api/users/me/` | IsAuthenticated | Get current user |
| `GET` | `/api/users/<id>/` | IsAuthenticated | Get user by ID |

### Patients

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| `GET` | `/api/users/patients/` | IsAdminUser | List all patients |
| `POST` | `/api/users/patients/` | IsAdminUser | Create patient profile |
| `GET` | `/api/users/patients/<id>/` | IsAdminUser | Get patient by ID |
| `PUT` | `/api/users/patients/<id>/` | IsAdminUser | Update patient profile |
| `PATCH` | `/api/users/patients/<id>/` | IsAdminUser | Partial update patient |
| `DELETE` | `/api/users/patients/<id>/` | IsAdminUser | Delete patient profile |

### Doctors

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| `GET` | `/api/users/doctors/` | IsAdminUser | List all doctors |
| `POST` | `/api/users/doctors/` | IsAdminUser | Create doctor profile |
| `GET` | `/api/users/doctors/<id>/` | IsAuthenticated | Get doctor by ID |
| `PUT` | `/api/users/doctors/<id>/` | IsAdminUser | Update doctor profile |
| `PATCH` | `/api/users/doctors/<id>/` | IsAdminUser | Partial update doctor |
| `DELETE` | `/api/users/doctors/<id>/` | IsAdminUser | Delete doctor profile |

### Lab Admins

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| `GET` | `/api/users/lab-admins/` | IsAdminUser | List all lab admins |
| `POST` | `/api/users/lab-admins/` | IsAdminUser | Create lab admin profile |
| `GET` | `/api/users/lab-admins/<id>/` | IsAdminUser | Get lab admin by ID |
| `PUT` | `/api/users/lab-admins/<id>/` | IsAdminUser | Update lab admin profile |
| `DELETE` | `/api/users/lab-admins/<id>/` | IsAdminUser | Delete lab admin profile |

### Files

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| `POST` | `/api/upload/` | IsAuthenticated | Upload a file to a receiver |
| `GET` | `/api/upload/unapproved/` | IsAuthenticated | List unapproved files for current user |
| `GET` | `/api/upload/approved/` | IsAuthenticated | List approved files for current user |
| `POST` | `/api/upload/<id>/approve/` | IsAuthenticated | Approve a file (receiver only) |

### Facilities

| Method | Endpoint | Permission | Description |
|--------|----------|------------|-------------|
| `GET/POST` | `/api/facilities/clinics/` | IsAdminUser | List/Create clinics |
| `GET/PUT/PATCH/DELETE` | `/api/facilities/clinics/<id>/` | IsAdminUser | Clinic detail |
| `GET/POST` | `/api/facilities/laboratories/` | IsAdminUser | List/Create labs |
| `GET/PUT/PATCH/DELETE` | `/api/facilities/laboratories/<id>/` | IsAdminUser | Lab detail |
| `GET/POST` | `/api/facilities/addresses/` | IsAdminUser | List/Create addresses |
| `GET/PUT/PATCH/DELETE` | `/api/facilities/addresses/<id>/` | IsAdminUser | Address detail |

---

## File Upload & Approval Workflow

### Uploading a File

**Request:**

```http
POST /api/upload/
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <binary_file>
receiver: <user_id>
```

**Response:**

```json
{
  "id": 1,
  "file": 1,
  "receiver": 2,
  "approved": false
}
```

### Listing Unapproved Files

Returns all files sent to the current user that haven't been approved yet.

```http
GET /api/upload/unapproved/
Authorization: Bearer <token>
```

### Approving a File

Only the receiver of the file can approve it.

```http
POST /api/upload/1/approve/
Authorization: Bearer <token>
```

**Success Response:**

```json
{
  "id": 1,
  "file": 1,
  "receiver": 2,
  "approved": true
}
```

**Error Responses:**

- `403 Forbidden` — You are not the receiver of this file
- `400 Bad Request` — File has already been approved

### Listing Approved Files

Returns all files the current user has approved.

```http
GET /api/upload/approved/
Authorization: Bearer <token>
```

---

## Testing with Resty

The project includes [Resty](https://github.com/micha/resty) client test files in the `resty/` directory for easy API testing.

### File Structure

```
resty/
├── auth.resty         # JWT token management
├── users.resty        # User & profile endpoints
├── files.resty        # File upload & approval
└── facilities.resty   # Clinics, laboratories & addresses
```

### Resty Conventions

- Use `###` as a splitter between requests
- Use `#<RequestName>` after `###` to mark favorites
- Use `@variable=value` to define variables
- Use Lua scripts to capture response data into variables

### Example: Capturing a Token

```resty
POST http://localhost:8000/api/token/
Content-Type: application/json

{
    "email": "admin@example.com",
    "password": "adminpass123"
}

--{%
  local body = ctx.json_body()
  ctx.set("auth.access_token", body.access)
  ctx.set("auth.refresh_token", body.refresh)
--%}
```

### Running Tests

1. **Start the Django server:**
   ```bash
   cd project
   python manage.py runserver
   ```

2. **Run auth tests first** (to populate token variables):
   ```bash
   resty resty/auth.resty
   ```

3. **Run other test files:**
   ```bash
   resty resty/users.resty
   resty resty/files.resty
   ```

### Variables Used

| Variable | Description |
|----------|-------------|
| `base_url` | API base URL (default: `http://localhost:8000`) |
| `auth.access_token` | Admin JWT access token |
| `auth.refresh_token` | Admin JWT refresh token |
| `user.access_token` | Regular user JWT access token |
| `user.refresh_token` | Regular user JWT refresh token |
| `files.upload_id` | Last uploaded file ID |
| `files.file_id` | Last file object ID |
| `facilities.clinic_id` | Last created clinic ID |
| `facilities.lab_id` | Last created laboratory ID |
| `facilities.address_id` | Last created address ID |

---

## Setup & Installation

### Prerequisites

- Python 3.12+
- pip
- virtualenv (recommended)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd tashkhees-backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt
   ```

4. **Run migrations:**
   ```bash
   cd project
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`.

---

## Environment Variables

For production, configure the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | *(development key)* |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hosts | `[]` |
| `DATABASE_URL` | Database connection URL | `sqlite:///db.sqlite3` |

---

## License

This project is part of the Mentorship Phase 2026.
