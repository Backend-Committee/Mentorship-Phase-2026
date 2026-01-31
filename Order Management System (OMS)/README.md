# Order Management System (OMS)

A comprehensive desktop-based Order Management System built with Python, CustomTkinter, and SQLAlchemy. This application is designed to help restaurants or businesses manage orders, menu items, categories, and users efficiently.

## Features

*   **Role-Based Access Control:**
    *   **Super Admin:** Full access, including user management.
    *   **Admin:** Manage menu items (plates) and categories.
    *   **Counter:** Access to the selling interface.
*   **Authentication:** Secure login system with hashed passwords (bcrypt).
*   **Selling Interface (POS):**
    *   Visual menu with product cards.
    *   Interactive shopping cart (Add, Increase/Decrease Quantity, Remove Items).
    *   Real-time total calculation.
    *   Order placement/Checkout.
*   **Admin Panel:**
    *   **Plates Management:** Add new plates with Name, Price, Description, Category, and Image. Delete existing plates.
    *   **Category Management:** Create and delete menu categories.
    *   **User Management:** (Super Admin only) Manage system users.
*   **Analysis:** Dashboard for viewing business insights (placeholder/feature).
*   **User Settings:** Change password functionality.
*   **Dynamic Updates:** Menu updates reflect immediately in the Selling view.

## Technologies Used

*   **Language:** Python 3
*   **GUI Framework:** CustomTkinter
*   **Database:** SQLite
*   **ORM:** SQLAlchemy
*   **Image Handling:** Pillow (PIL)
*   **Security:** bcrypt

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd "Order Management System (OMS)"
    ```

2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the Database:**
    Run the initialization script to set up the database and create the default super user.
    ```bash
    python init_db.py
    ```

## Usage

1.  **Run the Application:**
    ```bash
    python app.py
    ```

2.  **Login:**
    Use the default Super Admin credentials created by `init_db.py`:
    *   **Username:** `admin`
    *   **Password:** `admin123`

3.  **Getting Started:**
    *   Go to the **Admin Panel** to add Categories (e.g., "Starters", "Main Course") and Plates.
    *   Go to the **Selling** page to simulate taking an order.

## Project Structure

```
Order Management System (OMS)/
├── app.py              # Application entry point
├── init_db.py          # Database initialization script
├── requirements.txt    # Project dependencies
├── engin/              # Database engine configurations
├── gui/                # GUI components
│   ├── dashboard.py    # Main dashboard container
│   ├── login.py        # Login screen
│   └── pages/          # Individual pages (Selling, Admin, Analysis)
├── models/             # Database models (User, Plate, Order)
└── MetaData/           # Resource files (Images)
```

## Contributing

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## Auther
    -- **Name**: Mahmoud Adam
    -- **Email**: mahmoudadam5555@gmail.com

