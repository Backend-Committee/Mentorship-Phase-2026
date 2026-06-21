# InBuddy API Documentation

## Overview

InBuddy is a body composition tracking system that extracts metrics from body composition reports (images) using OCR, parses the text into structured data, and tracks measurements over time.

**Base URL:** `http://localhost:8000`

**Authentication:** All endpoints (except registration and login) require JWT Bearer token authentication.

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run migrations

```bash
cd inbuddy
python manage.py migrate
```

### 3. Create a superuser (optional, for admin panel)

```bash
python manage.py createsuperuser
```

### 4. Run the server

```bash
python manage.py runserver
```

---

## Authentication Flow

### Register a new user

```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "john",
    "password": "StrongPass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login (get JWT tokens)

```bash
curl -X POST http://localhost:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "StrongPass123!"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

### Refresh access token

```bash
curl -X POST http://localhost:8000/api/auth/jwt/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci..."
  }'
```

### Verify token

```bash
curl -X POST http://localhost:8000/api/auth/jwt/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGci..."
  }'
```

### Set token for subsequent requests

```bash
export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGci..."
```

All protected endpoints require the header:
```
Authorization: Bearer $TOKEN
```

---

## API Endpoints

### Users

#### Get current user profile

```
GET /api/users/profile/
```

**Response:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "john",
  "first_name": "John",
  "last_name": "Doe",
  "age": 28,
  "gender": "male",
  "height_cm": 175.5,
  "weight_kg": 78.0,
  "goal": "gain_muscle",
  "activity_level": "moderate",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-20T14:00:00Z"
}
```

#### Update current user profile

```
PATCH /api/users/profile/
```

**Request:**
```json
{
  "age": 29,
  "weight_kg": 80.0,
  "goal": "maintain"
}
```

All profile fields are optional — only send what you want to update.

#### Delete current user account

```
DELETE /api/users/profile/
```

**Field choices:**
- `gender`: `male`, `female`, `other`
- `goal`: `lose_weight`, `maintain`, `gain_muscle`, `improve_fitness`
- `activity_level`: `sedentary`, `light`, `moderate`, `active`, `very_active`

---

### Text Extraction (OCR)

#### List all extraction tasks

```
GET /api/extractions/
```

Query parameters:
- `page` — page number (default pagination, 20 per page)

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "image": "http://localhost:8000/media/extractions/2025/01/20/report.jpg",
      "extracted_text": "Body Fat: 18.5% ...",
      "status": "completed",
      "error_message": "",
      "created_at": "2025-01-20T12:00:00Z",
      "updated_at": "2025-01-20T12:00:05Z"
    }
  ]
}
```

#### Create extraction task (upload image)

```
POST /api/extractions/
```

**Request (multipart/form-data):**
```bash
curl -X POST http://localhost:8000/api/extractions/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "image=@/path/to/body_composition_report.jpg"
```

The OCR extraction runs **synchronously** during the request. Supported image formats: JPEG, PNG, BMP, TIFF, WebP.

**Response:**
```json
{
  "id": 4,
  "image": "http://localhost:8000/media/extractions/2025/01/20/report.jpg",
  "extracted_text": "Body Fat: 18.5%\nMuscle Mass: 35.2 kg\nBMI: 22.8\nWater: 55.0%\nVisceral Fat: 7\nBone Mass: 3.2 kg\nBasal Metabolism: 1650 kcal\nBody Age: 25",
  "status": "completed",
  "error_message": "",
  "created_at": "2025-01-20T12:00:00Z",
  "updated_at": "2025-01-20T12:00:05Z"
}
```

**Status values:** `pending`, `processing`, `completed`, `failed`

#### Get single extraction task

```
GET /api/extractions/<id>/
```

#### Delete extraction task

```
DELETE /api/extractions/<id>/
```

---

### Analysis

#### List all analyses

```
GET /api/analysis/
```

**Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "extraction_task": 4,
      "source_text": "Body Fat: 18.5% ...",
      "parsed_metrics": {
        "body_fat_percent": 18.5,
        "muscle_mass_kg": 35.2,
        "bmi": 22.8,
        "water_percent": 55.0,
        "visceral_fat": 7.0,
        "bone_mass_kg": 3.2,
        "basal_metabolism_kcal": 1650.0,
        "body_age": 25.0
      },
      "analyzed_at": "2025-01-20T12:01:00Z"
    }
  ]
}
```

#### Create analysis (parse body composition text)

```
POST /api/analysis/create/
```

**Request:**
```json
{
  "extraction_task": 4,
  "text": "Body Fat: 18.5%\nMuscle Mass: 35.2 kg\nBMI: 22.8\nWater: 55.0%\nVisceral Fat: 7\nBone Mass: 3.2 kg\nBasal Metabolism: 1650 kcal\nBody Age: 25"
}
```

`extraction_task` is optional. `text` is required.

**Response:**
```json
{
  "id": 3,
  "extraction_task": 4,
  "source_text": "Body Fat: 18.5% ...",
  "parsed_metrics": {
    "body_fat_percent": 18.5,
    "muscle_mass_kg": 35.2,
    "bmi": 22.8,
    "water_percent": 55.0,
    "visceral_fat": 7.0,
    "bone_mass_kg": 3.2,
    "basal_metabolism_kcal": 1650.0,
    "body_age": 25.0
  },
  "analyzed_at": "2025-01-20T12:01:00Z"
}
```

#### Parsed metrics keys

The parser extracts the following metrics from body composition report text:

| Key | Description | Example text patterns |
|---|---|---|
| `body_fat_percent` | Body fat percentage | `Body Fat: 18.5%`, `Fat Mass 18.5` |
| `muscle_mass_percent` | Muscle mass percentage | `Muscle Mass: 42%` |
| `muscle_mass_kg` | Muscle mass in kg | `Muscle Mass: 35.2 kg` |
| `bmi` | Body Mass Index | `BMI: 22.8` |
| `water_percent` | Body water percentage | `Water: 55.0%`, `Hydration 55%` |
| `visceral_fat` | Visceral fat level | `Visceral Fat: 7` |
| `bone_mass_kg` | Bone mass in kg | `Bone Mass: 3.2 kg` |
| `bone_mass_percent` | Bone mass percentage | `Bone Mass: 5.0%` |
| `basal_metabolism_kcal` | Basal metabolic rate | `Basal Metabolism: 1650 kcal`, `BMR 1650` |
| `body_age` | Metabolic/body age | `Body Age: 25` |
| `weight_kg` | Weight in kg | `Weight: 78.0 kg` |
| `protein_percent` | Protein percentage | `Protein: 18.5%` |
| `subcutaneous_fat` | Subcutaneous fat percentage | `Subcutaneous Fat: 12%` |
| `obesity_grade` | Obesity grade/level | `Obesity Grade: 1` |

The parser is case-insensitive and supports both English and Japanese/Chinese text patterns.

#### Get single analysis

```
GET /api/analysis/<id>/
```

#### Delete analysis

```
DELETE /api/analysis/<id>/
```

---

### Measurements

#### List all measurements

```
GET /api/measurements/
```

Query parameters:
- `date_from` — filter from date (YYYY-MM-DD)
- `date_to` — filter to date (YYYY-MM-DD)
- `page` — page number

**Example:**
```
GET /api/measurements/?date_from=2025-01-01&date_to=2025-01-31
```

**Response:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "user": 1,
      "date": "2025-01-20",
      "body_fat_percent": 18.5,
      "muscle_mass_kg": 35.2,
      "muscle_mass_percent": 42.0,
      "bmi": 22.8,
      "water_percent": 55.0,
      "visceral_fat": 7.0,
      "bone_mass_kg": 3.20,
      "basal_metabolism_kcal": 1650,
      "body_age": 25,
      "weight_kg": 78.0,
      "protein_percent": 18.5,
      "subcutaneous_fat_percent": 12.0,
      "notes": "After morning workout",
      "source_analysis": 3,
      "created_at": "2025-01-20T12:05:00Z",
      "updated_at": "2025-01-20T12:05:00Z"
    }
  ]
}
```

#### Create measurement

```
POST /api/measurements/
```

**Request:**
```json
{
  "date": "2025-01-20",
  "body_fat_percent": 18.5,
  "muscle_mass_kg": 35.2,
  "bmi": 22.8,
  "water_percent": 55.0,
  "visceral_fat": 7.0,
  "bone_mass_kg": 3.2,
  "basal_metabolism_kcal": 1650,
  "body_age": 25,
  "weight_kg": 78.0,
  "protein_percent": 18.5,
  "subcutaneous_fat_percent": 12.0,
  "notes": "After morning workout",
  "source_analysis": 3
}
```

Only `date` is required. All other fields are optional.

**Response:** Returns the created measurement object (same format as list response).

#### Get latest measurement

```
GET /api/measurements/latest/
```

Returns the most recent measurement (by date, then by creation time).

**Response:** Single measurement object or `404` if none exist.

#### Get single measurement

```
GET /api/measurements/<id>/
```

#### Update measurement

```
PATCH /api/measurements/<id>/
```

**Request:**
```json
{
  "body_fat_percent": 17.8,
  "notes": "Updated after re-measurement"
}
```

#### Delete measurement

```
DELETE /api/measurements/<id>/
```

---

## Complete Workflow Example

### 1. Register and login

```bash
# Register
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","username":"user","password":"Pass1234!","first_name":"Test","last_name":"User"}'

# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"Pass1234!"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['access'])")
```

### 2. Upload a body composition report image

```bash
curl -X POST http://localhost:8000/api/extractions/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "image=@report.jpg"
```

### 3. Analyze the extracted text

```bash
curl -X POST http://localhost:8000/api/analysis/create/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "extraction_task": 1,
    "text": "Body Fat: 18.5%\nMuscle Mass: 35.2 kg\nBMI: 22.8\nWater: 55.0%\nVisceral Fat: 7\nBone Mass: 3.2 kg\nBasal Metabolism: 1650 kcal\nBody Age: 25"
  }'
```

### 4. Save as a measurement

```bash
curl -X POST http://localhost:8000/api/measurements/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-01-20",
    "body_fat_percent": 18.5,
    "muscle_mass_kg": 35.2,
    "bmi": 22.8,
    "water_percent": 55.0,
    "visceral_fat": 7.0,
    "bone_mass_kg": 3.2,
    "basal_metabolism_kcal": 1650,
    "body_age": 25,
    "source_analysis": 1
  }'
```

### 5. View your latest measurement

```bash
curl -s http://localhost:8000/api/measurements/latest/ \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

## Error Responses

All errors follow DRF standard format:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

Validation errors:
```json
{
  "email": ["A user with that email already exists."],
  "password": ["This password is too short."]
}
```

## HTTP Status Codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created |
| 204 | No content (successful DELETE) |
| 400 | Bad request / validation error |
| 401 | Unauthorized (missing or invalid token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not found |

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DJANGO_SECRET_KEY` | (insecure default) | Django secret key |
| `DJANGO_DEBUG` | `True` | Debug mode |
| `DJANGO_ALLOWED_HOSTS` | `[]` | Comma-separated allowed hosts |
