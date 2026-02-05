🎓 School Management System

Database Design & Implementation using SQLite & Python

📌 Project Overview

This project is a School Management System designed to demonstrate:

Database analysis & design (ERD)

Relational database implementation using SQLite

Database operations using Python

Proper usage of Primary Keys, Foreign Keys, and JOINs

The system manages students, teachers, subjects, classes, and their relationships in a structured and efficient way.

🧩 Project Parts
🔹 Part 1: ERD Design

The ERD (Entity Relationship Diagram) represents the logical structure of the database and includes all required entities, attributes, and relationships.

📦 Main Entities

Student

Teacher

Subject

Class

Enrollment (Associative Entity)

Supervision (Associative Entity)

🔗 Relationships

A Student can enroll in many Subjects

A Subject can have many Students
→ Implemented using Enrollment (M–M relationship)

A Teacher can supervise many Students

A Student can be supervised by many Teachers
→ Implemented using Supervision (M–M relationship)

✅ ERD Requirements Applied

Primary Keys (PK)

Foreign Keys (FK)

Correct cardinalities (1–M, M–M)

Clear relationship labeling

📎 ERD Diagram

Designed using Draw.io / Miro / Lucidchart
(Attached as Image or PDF)

🗄️ Part 2: Database Implementation (SQLite + Python)
⚙️ Technologies Used

Python 3

SQLite3

JSON

🏗️ Database Schema
📘 Tables

Student

Teachers

Subjects

Classes

Enrollment

Supervision

🔑 Keys

Each table has a Primary Key

Foreign Keys enforce referential integrity

PRAGMA foreign_keys = ON is enabled

🔧 Features & Operations

The system supports all required database operations:

➕ Insert

Insert sample data into all tables

🔍 Select & JOIN

Retrieve enrolled students with their subjects using JOIN queries

✏️ Update

Update student information (e.g., address)

❌ Delete

Delete supervision records based on conditions

📤 Export

Export the entire database into a structured JSON file

📂 Project Structure
📁 School-Management-System
│
├── Management_System.db
├── School_Database.json
├── main.py
└── README.md

▶️ How to Run the Project

Clone the repository:

git clone <repository-link>


Run the Python file:

python main.py


Choose an option from the menu:

1. Insert Sample Data
2. Show Enrollment Report
3. Update & Delete Demo
4. Export Data to JSON
5. Exit

🧪 SQLite Commands Used

The following SQLite commands are implemented via Python:

CREATE TABLE

INSERT INTO

SELECT

UPDATE

DELETE

WHERE

JOIN

🎯 Learning Outcomes

Understanding database normalization

Designing ERD with correct relationships

Implementing relational databases using SQLite

Applying SQL commands through Python

Working with JSON data export

👩‍💻 Author

Eng. Habiba
School Management System Project
