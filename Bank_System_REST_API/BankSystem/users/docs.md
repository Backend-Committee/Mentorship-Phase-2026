# Users App Documentation

## Overview
The **Users App** is a core component of the Bank System REST API, responsible for:
- User Authentication (Registration, Login).
- User Management (CRUD operations).
- Role-based Access Control (RBAC).

## key Features
- **Custom User Model**: Extends Django's `AbstractUser` with role-based attributes.
- **Roles**:
  - `CUSTOMER`: Standard bank customers.
  - `TELLER`: Bank staff for transactions.
  - `MANAGER`: Branch managers.
  - `ADMIN`: System administrators.
  - `AUDITOR`: Compliance auditors.
- **API Endpoints**:
  - `/api/auth/register/`: Public registration.
  - `/api/mobile/users/`: Mobile app user interface.
  - `/api/office/users/`: Back-office user management.

## Technical Details

### Models
**`User`** (`users.models.User`)
- **Fields**:
  - `username`: Unique identifier.
  - `email`: User email.
  - `role`: One of the defined roles. Default is `CUSTOMER`.
  - `is_active`, `is_staff`: Standard Django flags.

### Serializers
1. **`UserSerializer`** (`users.serializers.UserSerializer`)
   - Used for retrieving and updating user details.
   - **Read-only fields**: `role`, `is_active` (cannot be changed via standard API).

2. **`UserRegistrationSerializer`** (`users.serializers.UserRegistrationSerializer`)
   - Used specifically for user creation.
   - Handles password hashing securely via `create_user`.
   - **Write-only fields**: `password`.

### Views
**`UserViewSet`** (`users.views.UserViewSet`)
- Handles listing, retrieving, and updating users.
- **Permissions**:
  - `create`: Open to public (uses `UserRegistrationSerializer`).
  - `list`: Restricted to `ADMIN` and `MANAGER` roles.
  - `retrieve/update`: Authenticated users (for their own profile) or Admins.
- **Logic**:
  - `get_serializer_class()` ensures `UserRegistrationSerializer` is used for creation, while `UserSerializer` is used for other actions.

**`RegisterView`** (`users.views.RegisterView`)
- Dedicated endpoint for user registration using `UserRegistrationSerializer`.

### Admin Interface
- **`CustomUserAdmin`**: updated to extend `UserAdmin` correctly.
- Adds `role` filter and display column to the admin list view.
- Fixes compatibility issues with Django's `UserAdmin` fieldsets.

## Testing
Unit tests are located in `users/tests/` and cover:
- Serializer validation.
- User registration flows.
- Permission enforcement on list views.

Run tests using:
```bash
python manage.py test users
```
