# Task 3 — Simple SQL CRUD CLI 


---

## What this script does (high level)

- Connects to a Microsoft SQL Server database using an ODBC connection string and SQLAlchemy's `create_engine`.
- Defines a `User` declarative model mapped to a `users` table.
- Provides functions: `create_user`, `select_user`, `select_users`, `update_user`, `delete_user`.
- Exposes a small interactive CLI menu to run the above operations from the terminal.

Contract (inputs / outputs)
- Inputs: user-provided values via the CLI (name, email, user id)
- Outputs: prints status messages and lists of users to stdout
- Error modes: invalid integers for IDs, missing DB driver, DB connection errors
- Success criteria: operations commit to the configured database and print confirmation

Edge cases considered
- Empty input handling when asking for integer IDs
- Duplicate email constraint (db will enforce unique email)
- Clean session close on program exit

---



## Key code (excerpts from `CRUD_DB.py`)

Connection & engine setup:

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=ZANATY;"
    "Database=stardb1;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

params = quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
```

Model definition and table creation:

```python
base = declarative_base()
class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

base.metadata.create_all(engine)
```

CRUD helpers (create example):

```python
Session = sessionmaker(bind=engine)
session = Session()

def create_user(name, email):
    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()
    print("User created")
```

CLI loop (shortened):

```python
if __name__ == "__main__":
    main()
```

(See `CRUD_DB.py` for the full implementation.)

---



## How to configure the database connection

The default `connection_string` in the script uses:

- ODBC Driver: `ODBC Driver 17 for SQL Server`
- Server: `ZANATY`
- Database: `stardb1`
- Trusted connection (Windows Integrated Auth) and `TrustServerCertificate=yes`

If your environment differs, update the string accordingly. Example for explicit SQL authentication:

```python
connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=MY_SERVER_NAME;"
    "Database=mydb;"
    "UID=db_user;"
    "PWD=db_password;"
)
```

For quick local testing without SQL Server, switch to SQLite by replacing the engine line with:

```python
engine = create_engine('sqlite:///task3_local.db', echo=False)
```

This will create `task3_local.db` in the current folder and allow you to test the CLI without installing ODBC drivers or using a remote SQL Server.

---

## Run the CLI

Activate your virtual environment then run:

```powershell
python CRUD_DB.py
```

You will see a menu:

```
Simple CRUD menu:
1) Create user
2) List users
3) Get user by id
4) Update user
5) Delete user
6) Exit
```

Examples:
- Create user: choose 1, provide name and email.
- List users: choose 2.
- Get by id: choose 3 and enter a numeric id.

Sample listing output:

```
1: Alice <alice@example.com>
2: Bob <bob@example.com>
```

---


