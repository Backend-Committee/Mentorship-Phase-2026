# 📚 Book Library Manager (Django)

---

## 🚀 Features

* **User Authentication:** Secure Registration and Login using **JWT** (JSON Web Tokens).
* **Security:** Password hashing using **Bcrypt**.
* **Book Exploration:** Fetch books from the [Gutendex API](https://gutendex.com/).
    * 🎲 Get a Random Book.
    * ⭐ Get the Highest Rated Book.
    * 📜 Get Oldest Book.
* **Favorites System:** Add books to your personal favorites list.
* **Custom Database:** Uses a local `users.json` file instead of SQL databases (NoSQL style).
* **Architecture:** Decoupled Frontend and Backend using REST API principles.

---

## 🛠️ Tech Stack

### Backend
* **Language:** Python 3.x
* **Framework:** Django & Django Rest Framework (DRF)
* **Authentication:** PyJWT (Manual implementation via Decorators)
* **Security:** Bcrypt
* **Database:** JSON File (`DB/users.json`)
* **Utilities:** Requests (for external API calls), Django-Cors-Headers

### Frontend
* **Structure:** HTML5
* **Styling:** CSS3
* **Logic:** Vanilla JavaScript (ES6+)
* **State Management:** LocalStorage (for Token)

---

## 📂 Project Structure

The project follows a specific structure designed to mimic a Node.js Express architecture:

```text
auth_library_python/
│
├── server.py                  # Entry point (runs the server on port 3000)
│
├── BackEnd/
│   ├── __init__.py
│   ├── settings.py            # Django settings (CORS, Apps)
│   ├── urls.py                # Main URL Router
│   ├── wsgi.py
│   │
│   ├── Controller/            # Logic for Auth and Books
│   │   ├── authController.py
│   │   └── bookController.py
│   │
│   ├── DB/                    # Data Storage
│   │   └── users.json         # The JSON Database
│   │
│   ├── middlewares/           # Custom Auth Middleware
│   │   └── auth_middlware.py
│   │
│   └── routes/                # API Routes definitions
│       ├── authRoutes.py
│       └── bookRoutes.py
│
└── FrontEnd/
    ├── css/
    │   └── style.css
    ├── Html/
    │   ├── login.html
    │   ├── register.html
    │   └── app.html
    └── js/
        ├── api.js             # API Configuration
        ├── auth.js
        ├── login.js
        ├── register.js
        └── app.js
