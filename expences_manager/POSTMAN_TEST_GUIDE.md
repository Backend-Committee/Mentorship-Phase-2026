# Expense Manager API - Postman Test Suite

## Overview
This Postman collection provides comprehensive testing coverage for the **Expense Manager API**, including:
- Authentication & Authorization
- Panel Management (Multi-tenant workspaces)
- Expense & Budget Operations
- Reports & Analytics (CSV/PDF/XLSX exports)
- Webhooks Integration
- Recurring Expenses
- Audit Logging
- Notifications & Preferences

**Total Endpoints**: 40+  
**Test Cases**: 70+ requests  
**Coverage**: Authentication, CRUD, Reporting, Exports, Advanced Features

---

## Setup Instructions

### 1. Import Collection into Postman
1. Download the collection file: `Expense_Manager_API.postman_collection.json`
2. Open Postman → **File** → **Import**
3. Select the JSON file and click **Import**

### 2. Configure Environment Variables

Create a new environment or update the existing collection variables:

**Key Variables to Set:**
- `base_url`: `http://localhost:8000/api` (or your deployment URL)
- `username`: Your test username
- `password`: Your test password
- `email`: Your test email

**Auto-populated Variables** (set automatically by tests):
- `access_token`: JWT access token (set after login)
- `refresh_token`: JWT refresh token (set after login)
- `panel_id`: Panel ID (set after panel creation)
- `category_id`: Category ID (set after category creation)
- `expense_id`: Expense ID (set after expense creation)
- `budget_id`: Budget ID (set after budget creation)
- `webhook_id`: Webhook ID (set after webhook creation)
- `schedule_id`: Schedule ID (set after schedule creation)
- `user_id`: Current user ID (set after login)

### 3. Start the Application

```bash
cd ExpenseManager
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://localhost:8000/api`

---

## Test Workflow

### Phase 1: Authentication
1. **Register User** - Create a new test account
2. **Login User** - Obtain JWT tokens (auto-saves to environment)
3. **Get Current User** - Verify authenticated session

### Phase 2: Panel & Workspace Setup
1. **Create Panel** - Create a new workspace/tenant
2. **List Panels** - View all user panels
3. **Get Panel Details** - Retrieve specific panel info
4. **List Panel Members** - View panel members
5. **Invite User by Email** - Send invitations

### Phase 3: Categories & Setup
1. **List Categories** - View default + custom categories
2. **Create Category** - Add new expense category
3. **Get Category** - Retrieve category details
4. **Update Category** - Modify category (color, name)

### Phase 4: Expenses & Budgets
1. **Create Expense** - Record an expense
2. **List Expenses** - View all expenses
3. **Update Expense** - Modify expense details
4. **List Expenses by Category** - Group by category
5. **Create Budget** - Set spending limits
6. **Check Budget Status** - Monitor budget health
7. **Update Budget** - Adjust limits/thresholds

### Phase 5: Reports & Analytics
1. **Report Summary (JSON)** - Get panel overview
2. **Report Summary (CSV)** - Export as CSV
3. **Report Summary (XLSX)** - Export as Excel
4. **Report Summary (PDF)** - Export as PDF
5. **Report Monthly** - Monthly trends
6. **Report Trends** - Category-level trends

### Phase 6: Advanced Features
1. **Create Recurring Expense** - Set up auto-expenses
2. **Create Webhook** - Register event handler
3. **Test Send Webhook** - Validate delivery
4. **Create Report Schedule** - Set up automated reports
5. **Run Schedule Now** - Trigger manual execution

### Phase 7: Notifications & Audit
1. **List Notifications** - View user notifications
2. **Mark Notification as Read** - Update read status
3. **List Audit Logs** - View system audit trail
4. **List Notification Preferences** - View delivery preferences

---

## Quick Start - Complete Test Flow

Follow this sequence to test the entire API:

```
1. Register User (Auth → Register User)
   ↓
2. Login User (Auth → Login User)
   ↓
3. Create Panel (Panels → Create Panel)
   ↓
4. Create Category (Categories → Create Category)
   ↓
5. Create Expense (Expenses → Create Expense)
   ↓
6. Create Budget (Budgets → Create Budget)
   ↓
7. Check Budget Status (Budgets → Check Budget Status)
   ↓
8. Report Summary (Reports → Report Summary JSON)
   ↓
9. Create Webhook (Webhooks → Create Webhook)
   ↓
10. Create Recurring Expense (Recurring → Create Recurring Expense)
   ↓
11. Create Report Schedule (Report Schedules → Create Schedule)
   ↓
12. List Audit Logs (Audit Logs → List Audit Logs)
```

---

## Export Formats

The API supports multiple export formats for reports:

### CSV Export
```
GET /reports/summary/?panel_id={{panel_id}}&export=csv
```
- Returns: `text/csv` content
- Usage: Spreadsheet import, data analysis

### XLSX Export
```
GET /reports/summary/?panel_id={{panel_id}}&export=xlsx
```
- Returns: Excel workbook format
- Usage: Professional reports, formatted data

### PDF Export
```
GET /reports/summary/?panel_id={{panel_id}}&export=pdf
```
- Returns: PDF document
- Usage: Sharing, printing, archival

---

## Authentication Details

### JWT Token Structure
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "panel_id": "660e8400-e29b-41d4-a716-446655440000",
  "role": "owner"
}
```

### Token Refresh
```
POST /auth/refresh/
Body: { "refresh": "{{refresh_token}}" }
```

### Logout with Token Blacklist
```
POST /auth/logout/
Body: { "refresh": "{{refresh_token}}" }
```

---

## Role-Based Access Control (RBAC)

The API enforces role-based permissions:

| Role | Permissions |
|------|------------|
| **Owner** | Create, read, update, delete all resources; manage members |
| **Editor** | Create, read, update expenses/budgets/categories |
| **Viewer** | Read-only access to expenses and reports |

**Test Scenario**: Invite a user as "viewer" and verify they cannot create expenses

---

## Webhook Testing

### Setup Webhook Test
1. Go to [webhook.site](https://webhook.site)
2. Copy your unique webhook URL
3. Create a webhook in Postman with that URL
4. Click "Test Send Webhook"
5. Check webhook.site for the delivery

### Webhook Events
Supported events for subscription:
- `expense.created` - When an expense is created
- `expense.updated` - When an expense is modified
- `expense.deleted` - When an expense is deleted
- `budget.exceeded` - When budget limit is exceeded
- `panel.invitation` - When user is invited
- `report.run` - When scheduled report runs

### Webhook Signature Verification
All webhooks include HMAC-SHA256 signature in header:
```
X-Webhook-Signature: sha256=<signature>
```

Verify signature:
```python
import hmac, hashlib
signature = hmac.new(
    secret.encode(),
    body.encode(),
    hashlib.sha256
).hexdigest()
assert signature == X-Webhook-Signature
```

---

## Bulk Testing Scenarios

### Scenario 1: Multi-user Collaboration
1. Create 2 user accounts
2. Create panel with User 1
3. Invite User 2 as "editor"
4. User 2 creates expenses
5. User 1 views audit trail
6. Verify User 2 cannot delete other's expenses

### Scenario 2: Budget Monitoring
1. Create budget with $500 limit, 80% alert threshold
2. Create 3 expenses totaling $420
3. Verify notification triggered
4. Create 1 more expense totaling $520
5. Verify "exceeded" notification

### Scenario 3: Report Scheduling
1. Create monthly report schedule (PDF format)
2. Set next_run_at to past date (triggers immediately)
3. Verify notification created
4. Check webhook received `report.run` event

### Scenario 4: Recurring Expenses
1. Create weekly recurring expense ($50)
2. Verify first instance created
3. Wait for next scheduled run (or manually trigger task)
4. Verify auto-created expense appears

---

## Performance Testing

### Load Test - Create 100 Expenses
```bash
# Run in Postman Collection Runner
1. Set iterations: 100
2. Use unique values: {{$randomInt}} for amounts
3. Monitor response times
4. Check for rate limiting (should not be exceeded at 1000/hour)
```

### Concurrent Users
```bash
# Simulate 10 concurrent users
1. Create 10 test accounts
2. Run collection for each user in parallel
3. Verify no data leakage between users
4. Check panel isolation enforcement
```

---

## Error Handling & Edge Cases

### Test Cases:
1. **Invalid Panel ID**: Try accessing non-existent panel
   - Expected: 404 Not Found

2. **Unauthorized Access**: Try accessing other user's panel
   - Expected: 403 Forbidden

3. **Invalid Budget Dates**: Set end_date before start_date
   - Expected: 400 Bad Request

4. **Duplicate Category**: Create category with same name in panel
   - Expected: 400 Bad Request (case-insensitive)

5. **Rate Limiting**: Make 1100 requests in 1 hour
   - Expected: 429 Too Many Requests

---

## Debugging Tips

### Enable Postman Console
- Press `Ctrl+Alt+C` (Windows) or `Cmd+Option+C` (Mac)
- View request/response details
- Check variable values

### Pre-request Scripts
All requests include dynamic variables:
- `{{$timestamp}}` - Unix timestamp for unique values
- `{{$randomUUID}}` - Random UUID
- `{{$isoTimestamp}}` - ISO formatted timestamp

### Response Assertions
Common test assertions in scripts:
```javascript
pm.test("Status code is 201", function() {
    pm.response.to.have.status(201);
});

pm.test("Response has ID", function() {
    pm.expect(pm.response.json()).to.have.property('id');
});
```

---

## Database Cleanup

After testing, clean up test data:

```bash
# Reset database to fresh state
python manage.py flush --noinput

# Re-run migrations
python manage.py migrate

# Create fresh test data via seed fixture (if available)
python manage.py loaddata fixtures/test_data.json
```

---

## API Documentation

For detailed endpoint documentation, visit:
```
Swagger UI: http://localhost:8000/api/schema/swagger/
ReDoc: http://localhost:8000/api/schema/redoc/
```

---

## Support & Troubleshooting

### Common Issues:

**"Invalid token" error**
- Solution: Run "Login User" request first to get fresh token

**"No such table" error**
- Solution: Run `python manage.py migrate`

**CORS errors**
- Solution: Ensure API is running on correct port (8000)

**Webhook not received**
- Solution: Use [webhook.site](https://webhook.site) or similar service
- Verify webhook is marked `is_active: true`

**Rate limit exceeded**
- Default: 1000/hour for authenticated users
- Wait 1 hour or adjust settings in `settings.py`

---

## Collection Structure

```
├── Authentication (5 endpoints)
├── Panels (7 endpoints)
├── Categories (5 endpoints)
├── Expenses (7 endpoints)
├── Budgets (6 endpoints)
├── Reports (6 endpoints)
├── Recurring Expenses (5 endpoints)
├── Webhooks (6 endpoints)
├── Report Schedules (5 endpoints)
├── Notifications (4 endpoints)
├── Notification Preferences (2 endpoints)
├── Audit Logs (2 endpoints)
├── Invitations (1 endpoint)
└── User Profile (2 endpoints)

Total: 70+ test requests
```

---

## Best Practices

1. **Always login first** - Obtain tokens before other requests
2. **Use dynamic variables** - Avoid hardcoded UUIDs
3. **Test error cases** - Not just the happy path
4. **Check audit logs** - Verify actions are recorded
5. **Verify webhooks** - Ensure integrations work
6. **Test with multiple users** - Verify RBAC enforcement
7. **Check exports** - Download and inspect generated files
8. **Monitor response times** - Identify performance bottlenecks

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | May 4, 2026 | Initial collection with all core features |

---

## Contact & Support

For issues or questions about the API:
- Check API documentation at `/api/schema/`
- Review audit logs for debugging
- Check error response messages
- Review test output in Postman console

---

**Happy Testing!** 🚀
