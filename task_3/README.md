# Students Manager (task_3) ✅

**Brief:** A simple command-line Students Manager that uses SQLite (via SQLAlchemy) to store students and provides basic CRUD operations through an interactive menu.

---

## Features 🔧

- Create a student (ID, full name, level)
- Update a student
- Delete a student
- Read a single student
- Read all students
- Basic input validation (integer checks, non-empty name, level range)
- Persistent storage in `database.db` (SQLite)

## Files

- `main.py` — main CLI program and data model (SQLAlchemy declarative model)
- `utils.py` — helper functions `get_opt` and `get_int` for safe user input
- `database.db` — created automatically when you run the program (SQLite file)

## Requirements ⚠️

- Python (3.8+ recommended)
- SQLAlchemy

Install dependency example:

```bash
pip install SQLAlchemy
```

## How to run ▶️

From the `task_3` folder run:

```bash
python main.py
```

You will see the menu:

```
WELCOME TO STUDENTS MANAGER

1- Create A Student
2- Update A Student
3- Delete A Student
4- Read A Student
5- Read All Students
```

Enter an option (1–5) and follow the prompts.