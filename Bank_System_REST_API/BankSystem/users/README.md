# Users App Documentation

This document explains the functionality and structure of the `users` app in the Bank System REST API.

## Overview
The `users` app handles user authentication, registration, and role management.

## Models
### `User`
- **Fields**:
    - `username`: Unique username.
    - `email`: User email address.
    - `password`: Encrypted password.
    - `role`: Role of the user (Customer, Teller, Manager, Admin, Auditor).
    - `is_active`: Boolean to check if the user is active.
    - `is_staff`: Boolean to check if the user is staff.

- **Roles**:
    - `CUSTOMER`: Regular customer user.
    - `TELLER`: Bank teller role.
    - `MANAGER`: Bank manager role.
    - `ADMIN`: Administrator role.
    - `AUDITOR`: Auditor role.

## Serializers
### `UserSerializer`
- Used for creating and retrieving user information.
- Handles password hashing during creation.

## Views
### `UserViewSet`
- Handles user CRUD operations.
- Permissions: Authenticated users can view/update their own profile. Admins can manage all users.

## Tests
- Comprehensive unit tests are located in `tests/`.
- To run tests: `python manage.py test users`
