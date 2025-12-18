# 📚 Library Management System (LMS)

A simple and efficient console-based Library Management System built with **Python** using Object-Oriented Programming (OOP) concepts. It handles books, users, and borrowing operations with automatic data saving.

## 🚀 Features

* **Data Persistence:** Automatically saves all data (books, users, transactions) to `library_data.pkl` using the `pickle` module.
* **Role-Based Access:**
    * **Worker:** Can add/remove books and register new customers or workers.
    * **Customer:** Can borrow and return books.
    * **Manager:** Has special privileges like viewing worker details and resetting the system.
* **Borrowing System:** Tracks book availability and current borrowers.

## 🔑 Default Admin Access
To log in as a Manager (Worker) for the first time, use the hardcoded ID:
* **Worker ID:** `666`
* **Role:** Manager/Admin

## 📂 Project Structure
* **Classes:** `Book`, `User`, `Customer`, `Worker`, `library`.
* **Files:**
    * `LMS.py`: Main application source code.
    * `library_data.pkl`: Database file (generated automatically upon execution).
