# Expense Manager API - Postman Quick Reference

## Files Included

1. **Expense_Manager_API.postman_collection.json** - Main API test collection (70+ endpoints)
2. **Expense_Manager_Local.postman_environment.json** - Local development environment
3. **Expense_Manager_Production.postman_environment.json** - Production environment
4. **POSTMAN_TEST_GUIDE.md** - Comprehensive testing guide

---

## Quick Import Steps

```bash
1. Download all 4 files
2. Open Postman
3. File → Import
4. Select collection JSON file
5. File → Import again for environment JSON
6. Select environment from dropdown (top-right)
7. Update base_url if needed
8. Start testing!
```

---

## Essential Endpoints Reference

### Authentication (No auth required)
```
POST /auth/register/          # Create account
POST /auth/login/             # Get tokens (stores access_token automatically)
POST /auth/refresh/           # Refresh expired token
POST /auth/logout/            # Invalidate token
POST /auth/password_reset/    # Request password reset
```

### Panels (Multi-tenant workspaces)
```
POST   /panels/               # Create panel
GET    /panels/               # List user's panels
GET    /panels/{id}/          # Get panel details
PATCH  /panels/{id}/          # Update panel
DELETE /panels/{id}/          # Delete panel
POST   /panels/{id}/members/  # List members
POST   /panels/{id}/invite_user/  # Invite user
```

### Expenses
```
POST   /expenses/             # Create expense
GET    /expenses/             # List expenses
GET    /expenses/{id}/        # Get expense
PATCH  /expenses/{id}/        # Update expense
DELETE /expenses/{id}/        # Delete (soft-delete)
GET    /expenses/by_category/ # Group by category
```

### Budgets
```
POST   /budgets/              # Create budget
GET    /budgets/              # List budgets
GET    /budgets/{id}/         # Get budget
PATCH  /budgets/{id}/         # Update budget
DELETE /budgets/{id}/         # Delete budget
GET    /budgets/check_status/ # Monitor spend vs limit
```

### Reports & Analytics
```
GET /reports/summary/         # Summary report (JSON/CSV/XLSX/PDF)
GET /reports/monthly/         # Monthly totals
GET /reports/trends/          # Category trends

# Add ?export=csv|xlsx|pdf for file formats
```

### Webhooks
```
POST   /webhooks/             # Create webhook
GET    /webhooks/             # List webhooks
GET    /webhooks/{id}/        # Get webhook
PATCH  /webhooks/{id}/        # Update webhook
DELETE /webhooks/{id}/        # Delete webhook
POST   /webhooks/{id}/test_send/  # Test webhook delivery
```

### Recurring Expenses
```
POST   /recurring-expenses/       # Create recurring expense
GET    /recurring-expenses/       # List
GET    /recurring-expenses/{id}/  # Get
PATCH  /recurring-expenses/{id}/  # Update
DELETE /recurring-expenses/{id}/  # Delete
```

### Notifications
```
GET    /notifications/            # List notifications
GET    /notifications/unread/     # Unread only
PATCH  /notifications/{id}/mark_as_read/     # Mark as read
PATCH  /notifications/mark_all_as_read/      # Mark all as read
```

### Other
```
GET /audit-logs/              # View audit trail
GET /categories/              # List categories
POST /report-schedules/       # Schedule reports
POST /invitations/accept/     # Accept panel invitation
```

---

## Query Parameters

### Date Filtering
```
?date_from=2026-05-01&date_to=2026-05-31
```

### Export Formats (Reports)
```
?export=json    (default)
?export=csv
?export=xlsx
?export=pdf
```

### Pagination
```
?page=1         # Default page number
```

### Search/Filter
```
?panel_id=<uuid>
?category_id=<uuid>
```

---

## Variable Substitution

Use these in Postman request bodies:

```javascript
{{base_url}}              # API base URL
{{access_token}}          # JWT access token
{{panel_id}}              # Current panel ID
{{category_id}}           # Current category ID
{{user_id}}               # Current user ID
{{$timestamp}}            # Unix timestamp (for unique names)
{{$randomUUID}}           # Random UUID
{{$isoTimestamp}}         # ISO formatted datetime
```

---

## Common Test Scenarios

### Scenario 1: Start Fresh (2 min)
```
1. Register User
2. Login User
3. Create Panel
4. Create Category
5. Create Expense
6. View Report Summary
```

### Scenario 2: Budget Management (3 min)
```
1. Login
2. Create Budget ($500/month)
3. Create Expense #1 ($200)
4. Create Expense #2 ($300)
5. Check Budget Status (should show 100% spent)
```

### Scenario 3: Multi-user Access (5 min)
```
1. User A: Create Panel & Category
2. User A: Invite User B as "viewer"
3. User B: Accept Invitation
4. User B: Try to create expense (should fail - viewer only)
5. User B: View expenses (should succeed)
6. User A: View audit trail (shows B's access)
```

### Scenario 4: Report Scheduling (3 min)
```
1. Create Report Schedule (Weekly, PDF format)
2. Click Run Schedule Now
3. Check webhooks received "report.run" event
4. Check notification created for user
```

---

## Error Codes Reference

| Code | Meaning | Fix |
|------|---------|-----|
| 401 | Unauthorized | Run "Login User" first |
| 403 | Forbidden | Check your role in panel |
| 404 | Not Found | Verify ID exists and panel_id is correct |
| 400 | Bad Request | Check request body format |
| 429 | Rate Limited | Wait 1 hour or adjust settings |
| 500 | Server Error | Check server logs |

---

## Authentication Flow

```
1. POST /auth/register/
   ↓ (creates new user)
   
2. POST /auth/login/
   ↓ (returns access_token & refresh_token)
   
3. Use access_token in "Authorization: Bearer {{access_token}}"
   ↓ (valid for 1 hour)
   
4. When expired: POST /auth/refresh/
   ↓ (returns new access_token)
   
5. Logout: POST /auth/logout/
   ↓ (blacklists refresh_token)
```

---

## Export Data

### Get Expense Report as CSV
```
GET /reports/summary/?panel_id={{panel_id}}&export=csv

# Response: File download (.csv)
# Save and open in Excel/Sheets
```

### Get Expense Report as XLSX
```
GET /reports/summary/?panel_id={{panel_id}}&export=xlsx

# Response: Excel workbook (.xlsx)
```

### Get Expense Report as PDF
```
GET /reports/summary/?panel_id={{panel_id}}&export=pdf

# Response: PDF document (.pdf)
```

---

## Webhook Testing

### Steps:
1. Go to https://webhook.site
2. Copy the unique webhook URL
3. Create webhook in Postman with that URL
4. Subscribe to event: `expense.created`
5. Create an expense
6. Check webhook.site for delivery

### Supported Events:
- `expense.created`
- `expense.updated`
- `expense.deleted`
- `budget.exceeded`
- `panel.invitation`
- `report.run`

---

## Performance Tips

### Run Multiple Tests (Load Testing)
```
Postman Collection Runner:
1. Click "Runner" button
2. Select collection
3. Select environment
4. Set iterations: 100
5. Click "Start Test"
```

### Monitor Response Times
```
Look at Postman console:
- Response time < 200ms (good)
- Response time > 500ms (investigate)
```

---

## Debugging

### Enable Console Output
```
Windows: Ctrl+Alt+C
Mac: Cmd+Option+C

Shows all request/response details
```

### Add Console Logs
```
Pre-request script:
console.log("Testing panel:", pm.environment.get("panel_id"));

Test script:
console.log("Response:", pm.response.json());
```

---

## Reset Environment

Clear all saved IDs to start fresh:
```
In Postman Environment:
- Set panel_id = ""
- Set category_id = ""
- Set expense_id = ""
- Set budget_id = ""
- Set webhook_id = ""
- Set schedule_id = ""
- Set access_token = ""
```

Then re-run from "Register User" → "Login User"

---

## Support Resources

- **Full Guide**: POSTMAN_TEST_GUIDE.md
- **API Docs**: http://localhost:8000/api/schema/swagger/
- **Swagger UI**: http://localhost:8000/api/schema/swagger/
- **ReDoc**: http://localhost:8000/api/schema/redoc/

---

## Cheat Sheet Commands

```bash
# Start Django dev server
python manage.py runserver

# Run tests
python manage.py test

# Create superuser
python manage.py createsuperuser

# Check API health
curl http://localhost:8000/api/

# View available endpoints
curl http://localhost:8000/api/
```

---

**Happy Testing!** 🎉
