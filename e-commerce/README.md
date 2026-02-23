# E-commerce Project

A comprehensive E-commerce platform built with Django that facilitates interactions between business owners and customers.
the project simulate the payment orders as will as owner panal 

## Features

- **User Roles**: The platform supports two distinct user types:
    - **Customers**: Can browse products, add items to cart, and place orders.
    - **Business Owners/Vendors**: Can manage their own product listings and view orders.

- **Product Management**:
    - Complete product catalog with categories (Electronics, Fashion, Home, etc.).
    - Product details including descriptions, pricing, stock management, and images.

- **Shopping Experience**:
    - Shopping Cart functionality.
    - Secure checkout process with stock validation.
    - Order tracking with status updates (Pending, Processing, Shipped, Delivered).

- **Order System**:
    - Detailed order history for users.
    - Order item tracking.

## Technologies Used

- **Backend**: Django (Python)
- **Database**: SQLite (Default)
- **Frontend**: HTML, CSS, Django Templates
- **Media**: Pillow for image handling

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd e-commerce
   ```

2. **Set up a virtual environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install django pillow
   ```

4. **Apply Migrations**
   Navigate to the project directory containing `manage.py`:
   ```bash
   cd Ecommerce
   python manage.py migrate
   ```

5. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**
   ```bash
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000/`.

## Application Structure

- **cart/**: Manages shopping cart functionality.
- **order/**: Handles order processing and tracking.
- **payment/**: Manages payment records and methods.
- **product/**: Handles product listings and categories.
- **user/**: Manages user authentication and profiles (Customer/Owner logic).
- **templates/**: HTML templates for the frontend.
- **static/**: CSS, JavaScript, and static images.

## Author

- **Name**: Mahmoud Adam
- **Email**: mahmoudadam5555@gmail.com


