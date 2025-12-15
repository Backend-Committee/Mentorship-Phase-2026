# Python JSON LMS

Lightweight command-line LMS that stores data as JSON files.

Usage
-----
Run the application from the project root:

```bash
python run.py
```

Features
--------
- Users CRUD operations (create, read, update, delete)
- Books CRUD operations (create, read, update, delete)
- Borrowing and returning books

Data layout
-----------
The app stores records under `users/` and `books/` and keeps `meta.json` files for ids.