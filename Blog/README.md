# Blog App

A simple blog application built with Django.

## Features

- User Registration and Login
- Create, Read, List Blog Posts
- User-specific "My Posts" view
- Admin interface integration

## Data Models

- **User**: Managed by Django's built-in authentication system.
- **Post**:
    - title: CharField
    - content: TextField
    - author: ForeignKey to User
    - created_at: DateTimeField
    - updated_at: DateTimeField

## Setup

1. **Install dependencies**:
   Ensure you have Django installed.
   ```bash
   pip install django
   ```

2. **Run Migrations**:
   The database has been reset to use the new Django User model.
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**:
   To access the admin panel.
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## Usage

- Navigate to `http://127.0.0.1:8000/` to see the home page.
- Register a new account or login.
- Create a new blog post.
- View "My Posts" to see your contributions.

## auther 
    - ** name **: Mahmoud Adam
    - ** email **: mahmoudadam5555@gmail.com 
