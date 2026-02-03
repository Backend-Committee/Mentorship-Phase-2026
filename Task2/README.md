# Task2: Authentication System

## Overview
This folder contains a simple, file-backed authentication system implemented in Python. It provides a minimal CLI to register and log in users. The project is intended for learning and demonstration — it is not production-ready.

Key points:
- Data is persisted to `users.json` as plain JSON.
- Email validation is performed using the `email_validator` package.
- Passwords are stored in plaintext (see Security notes below).

## Features
- Register users (username, email, password).
- Login users (email + password).
- Basic email format validation.
- Simple file-based persistence (`users.json`).

## Files and responsibilities
- `Auth_System.py` — Implements the `AuthSystem` class: loads/saves `users.json`, validates emails, registers and logs in users.
- `User.py` — `User` model: simple data holder with a `toDict()` method for JSON serialization.
- `main.py` — Small command-line interface (menu) to interact with the `AuthSystem`.
- `users.json` — Data file (created automatically after the first user registers). Example initial content:

```json
{
    "users": []
}
```

## Important code snippets
Here are a few representative snippets taken from the actual code to help you understand how the system works.

From `Auth_System.py` — registering and saving a user:

```python
    def saveUser(self,username,email,password):
        new_user = User(username,email,password)
        self.users.append(new_user)
        self.saveData()
        print("User registered successfully.")
```

From `Auth_System.py` — login flow and validation:

```python
    def loginUser(self,email,password):
        if not self.authenticateEmail(email):
            print("Email not found.")
            return False
        if not self.authanticatePassword(email,password):
            print("Incorrect password.")
            return False
        print("Login successful.")
        return True
```

From `main.py` — how the CLI interacts with the system:

```python
from Auth_System import AuthSystem

auth_system = AuthSystem()
# Register example
if auth_system.validateEmail("alice@example.com"):
    auth_system.registerUser("alice", "alice@example.com", "s3cret")

# Login example
auth_system.loginUser("alice@example.com", "s3cret")
```

## Api.py (example external API usage)

The `Api.py` script demonstrates a simple use of the `requests` library to fetch a random user from the public Random User API (https://randomuser.me/). It prints the HTTP status code, the full JSON response, and a couple of extracted fields.

Script (from `Task2/Api.py`):

```python
import requests

res = requests.get('https://randomuser.me/api/')

print(res.status_code)
print(res.json())
gender = res.json()['results'][0]['gender']
first_name = res.json()['results'][0]['name']['first']
print(gender)
print(first_name)
print(f'{first_name} as {gender}')
```

Example output (the exact output you shared):

```
200
{'results': [{'gender': 'female', 'name': {'title': 'Mrs', 'first': 'Jentje', 'last': 'Wamelink'}, 'location': {'street': {'number': 9637, 'name': 'Krollerweg'}, 'city': 'Hasselt', 'state': 'Friesland', 'country': 'Netherlands', 'postcode': '1698 XQ', 'coordinates': {'latitude': '30.8784', 'longitude': '110.7694'}, 'timezone': {'offset': '-8:00', 'description': 'Pacific Time (US & Canada)'}}, 'email': 'jentje.wamelink@example.com', 'login': {'uuid': '6f92ff53-f1c3-409b-a634-4ac2b3dcfeb7', 'username': 'goldenelephant687', 'password': 'capecod', 'salt': 'fVoaKSxy', 'md5': '8df06b31727b42f24d4e8792316b3a1b', 'sha1': 'c875948b5a3add922f0ff5e662814a85f2683c71', 'sha256': '60e1d68b6cacbca6fc70b142898235e3d2140546dfcb79cdb2ef169963489c17'}, 'dob': {'date': '1987-05-11T06:38:08.148Z', 'age': 38}, 'registered': {'date': '2004-10-13T21:59:15.534Z', 'age': 21}, 'phone': '(0858) 846433', 'cell': '(06) 73232947', 'id': {'name': 'BSN', 'value': '15435075'}, 'picture': {'large': 'https://randomuser.me/api/portraits/women/68.jpg', 'medium': 'https://randomuser.me/api/portraits/med/women/68.jpg', 'thumbnail': 'https://randomuser.me/api/portraits/thumb/women/68.jpg'}, 'nat': 'NL'}], 'info': {'seed': 'f7f37bb841f17aa6', 'results': 1, 'page': 1, 'version': '1.4'}}
female
Jentje
Jentje as female
```


