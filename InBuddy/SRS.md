
## Introduction
### Product scope
InBuddy let you see your progress, save your records, give your tips, Improve your life!

### Intended audience
Used by users that want to track their progress, build motivation, lose weight or reach goals

### Intended use
InBuddy will remind users to make in-body measurement and then give InBuddy the image/pdf of their in-body, then users can track their measurements and goals 

-------

## Functional requirements
### 1. User Authentication & Account Management

**Tech:** Django

#### Core Functions

- User registration (email + password, optional social login later)
- User login/logout
- Password reset (email-based)
- Token-based authentication (JWT recommended)
- User profile management:
    - Name, age, gender (optional but useful for analytics)
    - Height (important for body metrics context)
- Secure session handling

---

### 2. Data Input (Body Measurements Capture)

#### Supported Input Types

- Image upload (photos of body composition scans, reports)
- PDF upload (e.g., lab reports, InBody scan sheets)

#### Functional Requirements

- File upload system:
    - Accept formats: JPG, PNG, PDF
    - Max file size limit
- Preview before submission
- Store original file securely (cloud storage recommended)

---

### 3. AI Data Extraction Engine

#### Core Functionality

- Extract structured data from uploaded files using AI:
    - Weight
    - Body fat %
    - Muscle mass
    - BMI
    - Water %
    - Bone mass (if available)

#### Requirements

- OCR for images + PDFs
- AI parsing layer to map extracted text → structured fields
- Handle different report formats (flexible parsing rules)

#### Output Format Example

{  
  "weight": 72.5,  
  "body_fat": 18.2,  
  "muscle_mass": 55.1,  
  "date": "2026-03-25"  
}

---

### 4. Data Storage & Management

#### Functional Requirements

- Store extracted numeric data per user
- Allow manual editing after AI extraction
- Versioning (optional but valuable):
    - Keep original vs edited values
- Timestamp every entry

#### Database Models (high-level)

- User
- MeasurementRecord
- UploadedFile

---

### 5. Progress Tracking

#### Core Features

- Timeline of measurements
- Compare current vs previous data
- Highlight improvements or regressions

#### Metrics Tracking

- Weight trend
- Body fat trend
- Muscle gain/loss

---

### 6. Data Visualization

#### Functional Requirements

- Graphs for each metric over time
- Combined dashboard view

#### Suggested Charts

- Line charts (progress over time)
- Progress indicators (e.g., +2% muscle)

---

### 7. AI Insights & Recommendations

#### Smart Features

- AI-generated insights such as:
    - “You gained 1.5kg muscle in 2 weeks”
    - “Body fat decreased by 3% — great progress”

#### Optional Advanced Features

- Personalized tips:
    - Nutrition suggestions
    - Workout adjustments

---

### 8. Notifications & Reminders

#### Functional Requirements

- Remind users to upload new scans
- Notify on progress milestones

---

### 9. Security & Privacy

#### Requirements

- Secure file storage (encrypted)
- User data isolation
- GDPR-like compliance mindset
- Access control (users only see their data)

---

### 10. Admin Panel

#### Using Django Admin

- View users
- View uploaded files
- Monitor extracted data
- Flag incorrect AI results

---

### 11. API Layer (Backend)

#### Requirements

- REST API (using Django REST Framework)
- Endpoints:
    - Auth (login/register)
    - Upload file
    - Get measurements
    - Update measurements
    - Get analytics

---

### 12. Error Handling

#### Functional Requirements

- Handle failed uploads
- Handle AI extraction errors
- Allow user correction if AI fails

---

### 13. Scalability Considerations

- Async processing for AI (Celery + Redis recommended)
- Queue for file processing
- Cloud storage (AWS S3 or similar)

---

### 14. Future Enhancements (Optional but Smart)

- Integration with smart scales / wearables
- Social sharing / progress comparison
- Coach/trainer access
- Mobile app (React Native / Flutter)