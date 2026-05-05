# Expense Manager API Documentation

## Authentication Endpoints

### Register New User
- **POST** `/api/auth/register/`
- **Description**: Create a new user account
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }
  ```
- **Response**: User object + JWT tokens (access & refresh)

### Login
- **POST** `/api/auth/login/`
- **Description**: Obtain JWT access and refresh tokens
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "password": "SecurePass123",
    "panel_id": "optional-panel-uuid"
  }
  ```
- **Response**: `{ "access": "...", "refresh": "...", "user_id": "...", "panel_id": "...", "role": "..." }`

### Refresh Token
- **POST** `/api/auth/refresh/`
- **Description**: Get new access token using refresh token
- **Request Body**: `{ "refresh": "..." }`
- **Response**: `{ "access": "..." }`

---

## User Endpoints

### Get Current User Profile
- **GET** `/api/users/me/`
- **Authentication**: Required (Bearer token)

### Update User Profile
- **PUT/PATCH** `/api/users/update_profile/`
- **Authentication**: Required
- **Request Body** (partial):
  ```json
  {
    "username": "new_username",
    "email": "newemail@example.com"
  }
  ```

---

## Panel (Workspace) Endpoints

### List Panels (User's Panels)
- **GET** `/api/panels/`
- **Authentication**: Required
- **Response**: Array of panel objects with pagination

### Create Panel
- **POST** `/api/panels/`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "name": "My Project Budget"
  }
  ```

### Get Panel Details
- **GET** `/api/panels/{id}/`
- **Authentication**: Required

### Update Panel
- **PUT/PATCH** `/api/panels/{id}/`
- **Authentication**: Required (owner only)
- **Request Body**:
  ```json
  {
    "name": "Updated Panel Name"
  }
  ```

### Delete Panel
- **DELETE** `/api/panels/{id}/`
- **Authentication**: Required (owner only)

### List Panel Members
- **GET** `/api/panels/{id}/members/`
- **Authentication**: Required (panel member only)
- **Response**: Array of PanelUser objects

### Invite User to Panel
- **POST** `/api/panels/{id}/invite_user/`
- **Authentication**: Required (owner only)
- **Request Body**:
  ```json
  {
    "user_id": "uuid-of-user",
    "role": "editor"  // or "viewer", "owner"
  }
  ```

---

## Panel User (Membership) Endpoints

### List Panel Memberships
- **GET** `/api/panel-users/`
- **Authentication**: Required
- **Filter**: Shows only user's panel memberships

### Change Member Role
- **PATCH** `/api/panel-users/{id}/change_role/`
- **Authentication**: Required (panel owner only)
- **Request Body**:
  ```json
  {
    "role": "editor"
  }
  ```

### Remove Member from Panel
- **DELETE** `/api/panel-users/{id}/remove_member/`
- **Authentication**: Required (panel owner only)

---

## Category Endpoints

### List Categories
- **GET** `/api/categories/`
- **Authentication**: Required
- **Query Params**: `?panel_id=uuid` (optional filter)
- **Permissions**: User must be member of the panel

### Create Category
- **POST** `/api/categories/`
- **Authentication**: Required
- **Permissions**: Editor or owner of the panel
- **Request Body**:
  ```json
  {
    "panel": "uuid-of-panel",
    "name": "Food & Dining",
    "color_hex": "#FF5733",
    "is_default": false
  }
  ```

### Get Category Details
- **GET** `/api/categories/{id}/`
- **Authentication**: Required

### Update Category
- **PUT/PATCH** `/api/categories/{id}/`
- **Authentication**: Required (editor+ only)

### Delete Category
- **DELETE** `/api/categories/{id}/`
- **Authentication**: Required (editor+ only)

---

## Expense Endpoints

### List Expenses
- **GET** `/api/expenses/`
- **Authentication**: Required
- **Query Params**: `?panel_id=uuid` (optional)
- **Permissions**: User must be member of the panel
- **Note**: Soft-deleted expenses are excluded

### Create Expense
- **POST** `/api/expenses/`
- **Authentication**: Required
- **Permissions**: Editor or owner of the panel
- **Request Body**:
  ```json
  {
    "panel": "uuid-of-panel",
    "category": "uuid-of-category",
    "amount": "49.99",
    "date": "2026-05-02",
    "description": "Lunch with team"
  }
  ```

### Get Expense Details
- **GET** `/api/expenses/{id}/`
- **Authentication**: Required

### Update Expense
- **PUT/PATCH** `/api/expenses/{id}/`
- **Authentication**: Required (editor+ only)

### Delete Expense (Soft Delete)
- **DELETE** `/api/expenses/{id}/`
- **Authentication**: Required (editor+ only)
- **Note**: Sets `deleted_at` timestamp (soft delete)

### Get Expenses by Category
- **GET** `/api/expenses/by_category/?panel_id=uuid`
- **Authentication**: Required
- **Response**: Expenses grouped by category name

---

## Budget Endpoints

### List Budgets
- **GET** `/api/budgets/`
- **Authentication**: Required
- **Query Params**: `?panel_id=uuid` (optional)
- **Permissions**: User must be member of the panel

### Create Budget
- **POST** `/api/budgets/`
- **Authentication**: Required
- **Permissions**: Editor or owner of the panel
- **Request Body**:
  ```json
  {
    "panel": "uuid-of-panel",
    "category": "uuid-of-category",  // optional, null = panel-wide
    "limit_amount": "500.00",
    "period": "monthly",  // or "quarterly", "annual", "custom"
    "start_date": "2026-05-01",  // required if period is "custom"
    "end_date": "2026-05-31",    // required if period is "custom"
    "alert_threshold": 80  // percentage: alert at 80% of budget
  }
  ```

### Get Budget Details
- **GET** `/api/budgets/{id}/`
- **Authentication**: Required

### Update Budget
- **PUT/PATCH** `/api/budgets/{id}/`
- **Authentication**: Required (editor+ only)

### Delete Budget
- **DELETE** `/api/budgets/{id}/`
- **Authentication**: Required (editor+ only)

### Check Budget Status
- **GET** `/api/budgets/check_status/?panel_id=uuid`
- **Authentication**: Required
- **Response**: Array of budgets with:
  - `budget_id`: UUID
  - `limit`: Decimal amount
  - `spent`: Decimal amount spent
  - `status`: "on_track" | "warning" | "exceeded"

---

## Report Endpoints

### Summary Report
- **GET** `/api/reports/summary/?panel_id=uuid`
- **Authentication**: Required
- **Optional Query Params**: `date_from=YYYY-MM-DD`, `date_to=YYYY-MM-DD`
- **Response**: Panel summary with expense totals, category breakdown, and budget snapshot
- **Export**: add `export=csv|pdf|xlsx` to return file output instead of JSON

### Monthly Report
- **GET** `/api/reports/monthly/?panel_id=uuid`
- **Authentication**: Required
- **Optional Query Params**: `date_from=YYYY-MM-DD`, `date_to=YYYY-MM-DD`
- **Response**: Monthly buckets with `month`, `expense_count`, `total_spent`
- **Export**: add `export=csv|pdf|xlsx` to return file output instead of JSON

### Trends Report (Category by Month)
- **GET** `/api/reports/trends/?panel_id=uuid`
- **Authentication**: Required
- **Optional Query Params**: `date_from=YYYY-MM-DD`, `date_to=YYYY-MM-DD`, `category_id=uuid`
- **Response**: Trend rows with `month`, `category_name`, counts, totals, and month share percentage
- **Export**: add `export=csv|pdf|xlsx` to return file output instead of JSON

### Report Schedules
- **GET/POST** `/api/report-schedules/`
- **Authentication**: Required
- **Description**: Create recurring schedules for `summary`, `monthly`, and `trends` reports.
- **Request Body**:
  ```json
  {
    "panel": "uuid-of-panel",
    "report_type": "trends",
    "export_format": "xlsx",
    "frequency": "weekly",
    "category": "uuid-of-category",
    "date_from": "2026-01-01",
    "date_to": "2026-12-31",
    "next_run_at": "2026-05-10T09:00:00Z"
  }
  ```

### Run Scheduled Report Now
- **POST** `/api/report-schedules/{id}/run_now/`
- **Authentication**: Required
- **Description**: Marks schedule as executed and advances `next_run_at` based on frequency.

---

## Invitations

### Invite User (email)
- **POST** `/api/panels/{id}/invite_user/`
- **Authentication**: Required (owner only)
- **Request Body**: `{ "email": "invitee@example.com", "role": "viewer" }`
- **Response**: Invitation object (contains `token`)
- **Email Delivery**: enable SMTP with `USE_SMTP_EMAIL=1` and set `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and optional `EMAIL_USE_TLS` / `EMAIL_USE_SSL`.

### Accept Invitation
- **POST** `/api/invitations/accept/`
- **Authentication**: Required (must be the invited user)
- **Request Body**: `{ "token": "..." }`

---

## Notification Preferences

### List / Create / Update Preferences
- **GET/POST/PATCH/DELETE** `/api/notification-preferences/`
- **Authentication**: Required
- **Description**: Per-user, per-panel preferences for notification types and delivery methods (in-app, email).
---

## Audit Trail

### List Audit Logs
- **GET** `/api/audit-logs/`
- **Authentication**: Required
- **Query Params**: `?panel_id=uuid` (optional)
- **Description**: Read-only audit trail for actions such as panel changes, expenses, budgets, invitations, logins, logouts, and password resets.
---

## Auth Utilities

### Logout (revoke refresh token)
- **POST** `/api/auth/logout/`
- **Authentication**: Required
- **Request Body**: `{ "refresh": "<refresh_token>" }`

### Password Reset Request
- **POST** `/api/auth/password_reset/`
- **Authentication**: Not required
- **Request Body**: `{ "email": "user@example.com" }`

### Password Reset Confirm
- **POST** `/api/auth/password_reset_confirm/`
- **Authentication**: Not required
- **Request Body**: `{ "uid": "...", "token": "...", "new_password": "NewPass123" }`

---

## Notification Endpoints

### List Notifications
- **GET** `/api/notifications/`
- **Authentication**: Required
- **Filter**: Only current user's notifications

### Get Unread Notifications
- **GET** `/api/notifications/unread/`
- **Authentication**: Required

### Mark Notification as Read
- **PATCH** `/api/notifications/{id}/mark_as_read/`
- **Authentication**: Required

### Mark All Notifications as Read
- **PATCH** `/api/notifications/mark_all_as_read/`
- **Authentication**: Required

---

## Role-Based Access Control (RBAC)

### Roles and Permissions

| Action | Owner | Editor | Viewer |
|--------|-------|--------|--------|
| Create Expense | ✓ | ✓ | ✗ |
| View Expense | ✓ | ✓ | ✓ |
| Update Expense | ✓ | ✓ | ✗ |
| Delete Expense | ✓ | ✓ | ✗ |
| Create Category | ✓ | ✓ | ✗ |
| Create Budget | ✓ | ✓ | ✗ |
| Manage Members | ✓ | ✗ | ✗ |
| Delete Panel | ✓ | ✗ | ✗ |
| View Reports | ✓ | ✓ | ✓ |

---

## Error Responses

### Standard Error Format
```json
{
  "detail": "Error message",
  "field_name": ["Specific validation error"]
}
```

### Common HTTP Status Codes
- **200 OK**: Success
- **201 Created**: Resource created
- **400 Bad Request**: Validation error
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Permission denied (RBAC)
- **404 Not Found**: Resource not found
- **409 Conflict**: Duplicate resource or constraint violation

---

## Pagination

All list endpoints support pagination with default page size of 50.
- Query parameter: `?page=2`
- Response includes: `count`, `next`, `previous`, `results`

---

## Authentication Header

Include JWT token in all authenticated requests:
```
Authorization: Bearer <access_token>
```

Tokens expire after 60 minutes. Use refresh token to get new access token.
