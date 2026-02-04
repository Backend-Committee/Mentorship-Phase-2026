# MiniAuth – Simple Python Authentication System

MiniAuth is a lightweight authentication system built with Python.
It provides user registration and login functionality using a JSON file as a simple database, making it suitable for learning purposes, small projects, or CLI-based applications.

# 📌 Features

User registration with:

- Username

- Email

- Password

Email format validation using regular expressions

Password strength validation:

- Minimum 8 characters

- At least one uppercase letter

- At least one lowercase letter

- At least one digit

User login with email and password

Persistent storage using a JSON file

Fast user lookup using an in-memory index (dictionary)

Command-line interface (CLI)

# 📁 Project Structure

project/
│
├── auth.py # Main Python file
├── JSONFiles/
│ └── DB.JSON # JSON database (auto-created)
└── README.md

# ⚙️ How It Works

User data is stored in DB.JSON as a list of user objects.

When the program starts, data is loaded into memory as a dictionary indexed by email.

Registration adds a new user to the index and updates the JSON file.

Login checks credentials against the in-memory index for fast access.

# 🧩 Main Components

1. User Dataclass

Represents a user entity

2. MiniAuth Class

Handles:

- Database initialization

- Loading users from JSON

- Registering users

- Logging in users

Key methods:

- loadIndex() – Loads and indexes users from the JSON file

- register_user() – Registers a new user

- login_user() – Authenticates a user

- validate_user() – Checks if an email already exists

3. Validation Functions

CheckEmail(email)

- Ensures the email follows a valid format.

CheckPassword(password)

- Ensures the password is strong enough.

4. CLI Interface (main)

Provides a simple menu:

1. Register
2. Login
3. Exit

# ▶️ How to Run

Make sure Python 3.8+ is installed

Run the file:

python auth.py

Follow the on-screen instructions

# 🧪 Example Usage

auth = MiniAuth()
auth.register_user("testuser", "Password123", "test@example.com")
auth.login_user("test@example.com", "Password123")

# ⚠️ Important Notes

This project is for learning and demonstration purposes only.

Not suitable for production use without improvements.

# 🚀 Possible Improvements

Hash passwords using bcrypt or hashlib

Add password confirmation during registration

Add account deletion or update features

Replace JSON with a real database (SQLite, PostgreSQL)

Integrate with a web framework like Django or Flask

# 📄 License

This project is open for educational use and modification.
