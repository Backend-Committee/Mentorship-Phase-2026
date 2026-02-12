# School Management System

A simple yet powerful **School Management System** built with Python and SQLite.  
Manages students, teachers, classes, subjects, enrollments, and teacher assignments with full CRUD operations and a clean console menu.

Perfect for college projects, learning databases, or as a starting point for a real school admin tool.

## Features

- Full **CRUD** (Create, Read, Update, Delete) for:
  - Students
  - Teachers
  - Subjects
  - Classes
- Many-to-many relationships handled properly:
  - Classes ↔ Subjects (via `class_subjects`)
  - Students enroll in specific class-subject combos
  - Teachers assigned to specific class-subject combos
- Enroll students in subjects within a class
- Assign grades to enrollments
- View students with their enrolled subjects, classes, grades & status
- Sample data insertion for quick testing
- User-friendly console menu (24 options!)
- Proper foreign keys, unique constraints, and error handling

## Database Schema (ERD Summary)

- **students** → student_id (PK), first_name, last_name, dob, gender, email (unique), phone
- **teachers** → teacher_id (PK), first_name, last_name, email (unique), phone, hire_date
- **subjects** → subject_id (PK), name (unique), credits
- **classes** → class_id (PK), name, grade_level, academic_year
- **class_subjects** (junction) → class_subject_id (PK), class_id (FK), subject_id (FK) — unique pair
- **enrollments** → enrollment_id (PK), student_id (FK), class_subject_id (FK), enrolled_on, status, final_grade — unique per student+class_subject
- **teacher_assignments** → assignment_id (PK), teacher_id (FK), class_subject_id (FK), role, assigned_on — unique per teacher+class_subject

(You can draw the full ERD using Draw.io / Lucidchart based on this structure)

## Requirements

- Python 3.8+
- No external packages needed (only built-in `sqlite3`)

## Installation & Usage

1. Clone or download the project
   ```bash
   git clone https://github.com/yourusername/school-management-system.git
   cd school-management-system
   ```
