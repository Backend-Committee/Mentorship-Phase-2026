# \# Library Management System (Python OOP)

# 

# \## 📚 Project Overview

# This is a simple \*\*Library Management System\*\* implemented in \*\*Python\*\* using \*\*Object-Oriented Programming (OOP)\*\* concepts.

# The system allows you to manage books, users, and the borrowing/returning process.

# 

# ---

# 

# \## 🎯 Objective

# Create a simple library system that can:

# 

# \- Manage books

# \- Manage users

# \- Allow borrowing and returning books

# \- Display available books

# 

# ---

# 

# \## 🏗️ Features

# The system includes:

# 

# 1\. \*\*Add a Book\*\* – Add new books to the library.

# 2\. \*\*Add a User\*\* – Register new users.

# 3\. \*\*Borrow Book\*\* – Allow a user to borrow a book if it’s available.

# 4\. \*\*Return Book\*\* – Allow a user to return a borrowed book.

# 5\. \*\*Display Available Books\*\* – Show all books that are currently available.

# 

# ---

# 

# \## 🧩 Classes \& Methods

# 

# \### \*\*Book\*\*

# Represents a book in the library.

# 

# \- `\\\_\\\_init\\\_\\\_(self, title, author, is\\\_available=True)` – Initialize a book.

# \- `disPlay\\\_info(self)` – Display book information.

# 

# \### \*\*User\*\*

# Represents a library user.

# 

# \- `\\\_\\\_init\\\_\\\_(self, name, user\\\_id)` – Initialize a user.

# \- `display\\\_info(self)` – Display user information including borrowed books.

# 

# \### \*\*Library\*\*

# Handles all library operations.

# 

# \- `add\\\_book(self, book)` – Add a book to the library.

# \- `add\\\_user(self, user)` – Add a user to the library.

# \- `borrow\\\_book(self, book, user)` – Borrow a book for a user.

# \- `return\\\_book(self, book, user)` – Return a borrowed book.

# \- `display\\\_available\\\_books(self)` – Print all available books.

# 

# ---

# 

# \## 💻 How to Run

# 1\. Make sure you have \*\*Python 3.x\*\* installed.

# 2\. Run the script in your terminal or Python IDE:

# ```bash

# python Backend\_projects.py





--- Library Menu ---

1\. Add Book

2\. Add User

3\. Borrow Book

4\. Return Book

5\. Display Available Books

6\. Exit

Enter your choice: 1

Enter book title: Python Basics

Enter book author: John Doe

Book added successfully

