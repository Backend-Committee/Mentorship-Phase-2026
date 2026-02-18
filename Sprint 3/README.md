# Gym Class Booking System (Python + MySQL)

## Project Overview
This project is a **Gym Class Booking System** implemented using **Python** and **MySQL**, designed to demonstrate full **CRUD (Create, Read, Update, Delete)** operations as required in **Project 3 – SQL CRUD Operations**.

The system allows managing:
- Gym Members
- Gym Classes
- Class Bookings

It uses a **menu-driven CLI interface** and connects Python to a relational database using the `mysql-connector-python` library.

---

## Project Objectives
- Understand CRUD fundamentals
- Practice database design and relationships
- Integrate Python with an SQL database
- Implement input validation
- Work with foreign key relationships

---

## Technologies Used
- **Python 3**
- **MySQL**
- **mysql-connector-python**

---

![Database Schema](Database Schema.jpg)
```
project/
│
├── Create Schema.py      # Create database
├── Gym booking interface.py        # Create tables
├── main.py                # CRUD logic & menus
└── README.md
```

---

## Installation & Setup

### 1. Install MySQL Connector
```bash
pip install mysql-connector-python
```

### 2. Configure Database Credentials
Update the following values in the Python files if needed:
```python
host="localhost"
user="root"
```

### 3. Create Database
Run:
```bash
python Main.py
```

### 4. Create Tables
Run:
```bash
python Create Schema.py
```

---

## CRUD Operations

### Member CRUD
- **Create**: Add new gym member
- **Read**:
  - View all members
  - View member by ID
- **Update**: Modify member name or phone number
- **Delete**: Remove member from database

### Class CRUD
- **Create**: Add new gym class
- **Read**:
  - View all classes
  - View class by ID
- **Update**: Modify class name, duration, or day
- **Delete**: Remove class

### Booking CRUD
- **Create**: Book a class for a member
- **Read**:
  - View all bookings
  - View by booking ID
  - View by member ID
  - View by class ID
- **Delete**: Cancel booking

---

## Input Validation
Validation functions ensure:
- Names are not empty and within length limits
- Duration and IDs are numeric
- Booking dates are valid

This prevents invalid data insertion into the database.

---

## User Interface
The system uses a **text-based menu**:

### Main Menu
```
1) Manage Members
2) Manage Classes
3) Manage Bookings
4) Exit
```

Each section contains its own CRUD submenu.

---

## Example Usage
```text
Enter choice: 1
Enter member name: Ahmed
Enter phone number: 0123456789
Member added successfully.
```

---

## Notes & Limitations
- Hard delete is used (no soft delete)
- No authentication or role-based access
- Console-based (no GUI)


---

## Author
**Zeyad Amin**

---

This project fulfills all requirements of **Project 3 – SQL CRUD Operations**.

