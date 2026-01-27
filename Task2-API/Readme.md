# User Registration API - Architecture

## Project Structure

```
project-root/
├── main.py                 # Flask application & routes
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── Templates/
│   └── register.html      # Registration form UI
├── Static/
│   └── styles.css         # Styling
└── Database/
    └── users.json         # User data storage
```

## Components

### Backend (Flask)

- **Routes**: User registration endpoint (`POST /`)
- **Database**: JSON file storage for users
- **Validation**: Email uniqueness check

### Frontend

- **Form**: HTML registration form with fields:
  - Username
  - Email
  - Password

## Recommended Improvements

- Add input validation & sanitization
- Hash passwords before storing
- Use proper database (SQLite/PostgreSQL)
- Separate concerns (models, routes, utilities)
- Add error handling & logging
- Implement authentication (JWT/sessions)

