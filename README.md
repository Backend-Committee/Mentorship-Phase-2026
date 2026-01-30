
---

# 🏋️‍♂️ Gym Management System (Backend-Focused)

## 📌 Project Overview

This project is a robust Command Line Interface (CLI) application for managing gym operations, developed as part of the **Mentorship Phase 2026**. It focuses on implementing high-quality Backend standards, including **Relational Database Design**, **Data Integrity**, and **Object-Relational Mapping (ORM)**.

## 🏗️ Technical Architecture

The system is built with a modular architecture to ensure a clean **Separation of Concerns**:

* **Database Configuration (`db.py`)**: Manages the connection pool and session lifecycle using SQLAlchemy.
* **Data Modeling (`models.py`)**: Defines the schema using modern SQLAlchemy Declarative Mapping.
* **Application Logic (`main.py`)**: The engine containing the interactive menu and core business logic.

## 🚀 Key Features & Implementation

### 1. Data Normalization (3rd Normal Form - 3NF)

The database was designed from the ground up following **3NF** principles to eliminate redundancy:

* **1NF**: Atomic attributes (e.g., decomposing "Name" into `first_name` and `last_name`).
* **2NF**: All non-key attributes are fully dependent on the Primary Key.
* **3NF**: Elimination of transitive dependencies by isolating membership details into a separate `Plans` table.

### 2. Advanced CRUD with Validation

* **Create**: Validates inputs using **Regular Expressions (Regex)** for emails and data-type checks for numeric fields.
* **Read**: Efficiently retrieves records using SQLAlchemy filters.
* **Update**: Implements partial update logic that preserves existing data for blank inputs.
* **Soft Delete**: Utilizes an `is_deleted` flag to protect data from accidental permanent removal, supporting future **Data Engineering** tasks.

### 3. Smart Relationship Management

Utilizes `relationship` and `back_populates` for bidirectional data navigation:

* **Plan ↔ Member**: Access all members of a plan via `plan.members`.
* **Member ↔ Payment**: Automatic cleanup of payments via `cascade="all, delete-orphan"` when a member is removed.

### 4. Session & State Management

Implements `session.refresh()` and `session.expire_all()` to ensure the application UI consistently reflects the latest database state, overcoming common ORM caching hurdles.

## 🛠️ Tech Stack

* **Language**: Python 3.x
* **ORM**: SQLAlchemy
* **Database**: SQLite (gym.db)
* **Design Pattern**: Repository-inspired functional CRUD

## 📥 Installation & Usage

1. **Clone the Repository**:
```bash
git clone https://github.com/Ahmed-Sheref/gym-backend.git
cd gym-backend

```


2. **Install Dependencies**:
```bash
pip install sqlalchemy

```


3. **Run the Application**:
```bash
python main.py

```



## 📊 Database Schema Overview

| Entity | Description | Key Attributes |
| --- | --- | --- |
| **Plan** | Membership Tiers | `plan_id` (PK), `plan_name`, `price` |
| **Member** | Gym Clients | `member_id` (PK), `email`, `plan_id` (FK) |
| **Payment** | Financial Logs | `payment_id` (PK), `amount`, `member_id` (FK) |

## 👨‍💻 Author

**Ahmed Sheref**

* **Education**: 3rd Year Information Systems Student at Cairo University.
* **Focus**: Backend Engineering (Python/Node.js), Data Engineering, and Competitive Programming.

---
