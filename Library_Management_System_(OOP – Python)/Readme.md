========================================
        LIBRARY MANAGEMENT SYSTEM
========================================

----------------------------------------
OVERVIEW
----------------------------------------
A Python-based Library Management System used to manage books and users.
The system allows users to borrow, return, and view books.
All data is stored in a JSON file for persistence.
The project is built using Object-Oriented Programming (OOP) concepts
with the following classes:
- Book
- User
- Library

----------------------------------------
FEATURES
----------------------------------------
- Borrow a Book: Allows users to borrow available books
- Return a Book: Allows users to return borrowed books
- View Books: Displays all available books in the library
- Save Data: Saves library data to a JSON file

----------------------------------------
SETUP & RUN
----------------------------------------
1) Download the file: library_system.py
2) Open Terminal / Command Prompt
3) Run the program using:

   python library_system.py

4) A menu will appear to choose actions:
   - Borrow a book
   - Return a book
   - Show books
   - Exit

----------------------------------------
SYSTEM CLASSES
----------------------------------------

[1] BOOK CLASS
----------------------------------------
Description:
Represents a single book in the library.

Attributes:
- id        : Book unique ID
- title     : Book title
- author    : Book author
- category  : Book category
- pages     : Number of pages
- status    : Availability (True / False)

Methods:
- summary() : Returns book summary
- to_json() : Converts book data to JSON format

----------------------------------------

[2] USER CLASS
----------------------------------------
Description:
Represents a user who can borrow books.

Attributes:
- id             : User ID
- name           : User name
- email          : User email
- phone          : User phone number
- borrowed_books : List of borrowed books

Methods:
- add_book()     : Add book to borrowed list
- remove_book()  : Remove book from borrowed list
- to_json()      : Converts user data to JSON format

----------------------------------------

[3] LIBRARY CLASS
----------------------------------------
Description:
Manages the entire library system.

Attributes:
- name  : Library name
- books : List of books
- users : List of users

Methods:
- add_book()                : Add a new book
- add_user()                : Add a new user
- search_book_and_borrow()  : Borrow a book
- return_book()             : Return a book
- show_books()              : Display all books
- save_to_file()            : Save data to JSON file

----------------------------------------
EXAMPLE JSON OUTPUT
----------------------------------------
{
  "name": "My Library",
  "books": [
    {
      "ID": 1,
      "title": "Clean Code",
      "author": "Robert Martin",
      "category": "Software",
      "pages": 464
    }
  ],
  "users": [
    {
      "id": 10,
      "name": "Ahmed",
      "email": "ahmedshalhadad1@gmail.com",
      "phone": "01091575793",
      "borrowedBooks": []
    }
  ]
}

----------------------------------------
USAGE
----------------------------------------
1) Borrow a Book
   - Choose option 1
   - Enter user ID
   - Enter book title

2) Return a Book
   - Choose option 2
   - Enter user ID
   - Enter book ID

3) Show Books
   - Choose option 3

4) Exit
   - Choose option 4

----------------------------------------
LICENSE
----------------------------------------
MIT License
Open-source project
