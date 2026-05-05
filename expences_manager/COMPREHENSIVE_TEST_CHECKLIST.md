# Expense Manager API - Comprehensive Testing Checklist

## Pre-Test Setup

- [ ] Django development server running on `http://localhost:8000`
- [ ] Postman installed with collection imported
- [ ] Environment set to "Expense Manager Local"
- [ ] `base_url` configured correctly
- [ ] Database migrated (`python manage.py migrate`)
- [ ] Fresh database (optional: `python manage.py flush --noinput`)

---

## Phase 1: Authentication Testing

### User Registration
- [ ] Register new user with valid credentials
  - Username: `testuser1`
  - Email: `testuser1@example.com`
  - Password: `SecurePass123`
  - Expected: 201 Created
- [ ] Register with duplicate username → Expected: 400 Bad Request
- [ ] Register with weak password → Expected: 400 Bad Request
- [ ] Register with invalid email → Expected: 400 Bad Request

### User Login
- [ ] Login with correct credentials
  - Expected: 200 OK
  - Response includes: `access`, `refresh`, `user_id`, `panel_id`, `role`
  - `access_token` auto-saved to environment
- [ ] Login with wrong password → Expected: 401 Unauthorized
- [ ] Login with non-existent user → Expected: 401 Unauthorized
- [ ] Verify JWT contains claims: `user_id`, `panel_id`, `role`

### Token Management
- [ ] Refresh token with valid refresh token → Expected: 200 OK
- [ ] Refresh token with invalid token → Expected: 401 Unauthorized
- [ ] Logout with valid token → Expected: 200 OK
- [ ] Use blacklisted token → Expected: 401 Unauthorized

### Password Reset Flow
- [ ] Request password reset with valid email → Expected: 200 OK
- [ ] Request password reset with non-existent email → Expected: 400 Bad Request
- [ ] Confirm password reset with valid token → Expected: 200 OK
- [ ] Login with new password → Expected: 200 OK
- [ ] Old password no longer works → Expected: 401 Unauthorized

### User Profile
- [ ] Get current user profile → Expected: 200 OK
- [ ] Update profile (name, email) → Expected: 200 OK
- [ ] Verify changes persisted → Expected: 200 OK with updated data

---

## Phase 2: Panel Management (Multi-tenant)

### Panel CRUD
- [ ] Create new panel
  - Name: `Test Workspace 1`
  - Description: `Testing panel`
  - Expected: 201 Created, returns panel_id
  - `panel_id` auto-saved to environment
- [ ] List all user panels → Expected: 200 OK, returns array
- [ ] Get panel details → Expected: 200 OK
- [ ] Update panel (name, description) → Expected: 200 OK
- [ ] Delete panel → Expected: 204 No Content
- [ ] Verify panel deleted from list → Expected: 404 on GET

### Default Categories
- [ ] Create panel → Expected: 10 default categories auto-created
- [ ] List categories → Expected: includes Food, Transportation, Entertainment, etc.
- [ ] Verify colors assigned → Expected: each category has hex color

### Panel Membership
- [ ] Get panel members → Expected: 200 OK
- [ ] Verify owner is current user
- [ ] List members in empty panel → Expected: 1 member (owner)

### Multi-panel Isolation
- [ ] Create panel with User A
- [ ] Create panel with User B
- [ ] User A tries to access User B's panel → Expected: 403 Forbidden
- [ ] User A's list shows only own panel → Expected: 1 panel
- [ ] User B's list shows only own panel → Expected: 1 panel

---

## Phase 3: Invitations & Access Control

### Email Invitations
- [ ] Invite user by email to panel
  - Email: `newuser@example.com`
  - Role: `editor`
  - Expected: 201 Created, invitation_token returned
- [ ] Resend invitation → Expected: 200 OK
- [ ] Accept invitation with valid token
  - Register new account if needed
  - POST to `/invitations/accept/` with token
  - Expected: 200 OK, user added as `editor`
- [ ] Accept invitation with invalid token → Expected: 400 Bad Request
- [ ] Accept same invitation twice → Expected: 400 Bad Request

### Direct Invite (Link/Token)
- [ ] Create panel user invitation directly
- [ ] Get invitation token from response
- [ ] Accept using token as different user
- [ ] Verify new user has correct role in panel

### Role-Based Access Control
- [ ] Create panel as User A (role: owner)
- [ ] Invite User B as editor
- [ ] Invite User C as viewer

#### Owner Permissions (User A)
- [ ] Create expense → Expected: 201 OK
- [ ] Update expense → Expected: 200 OK
- [ ] Delete expense → Expected: 204 OK
- [ ] Create budget → Expected: 201 OK
- [ ] Create category → Expected: 201 OK
- [ ] Invite users → Expected: 201 OK
- [ ] Update panel → Expected: 200 OK
- [ ] Delete panel → Expected: 204 OK

#### Editor Permissions (User B)
- [ ] Create expense → Expected: 201 OK
- [ ] Update expense → Expected: 200 OK
- [ ] Delete expense → Expected: 204 OK
- [ ] Create budget → Expected: 201 OK
- [ ] Try to delete panel → Expected: 403 Forbidden
- [ ] Try to invite users → Expected: 403 Forbidden

#### Viewer Permissions (User C)
- [ ] List expenses → Expected: 200 OK
- [ ] View expense → Expected: 200 OK
- [ ] Create expense → Expected: 403 Forbidden
- [ ] Update expense → Expected: 403 Forbidden
- [ ] Delete expense → Expected: 403 Forbidden
- [ ] View reports → Expected: 200 OK
- [ ] Create budget → Expected: 403 Forbidden

---

## Phase 4: Categories

### Category CRUD
- [ ] List default categories → Expected: 200 OK, 10+ categories
- [ ] Create custom category
  - Name: `Entertainment`
  - Color: `#FF5733`
  - Expected: 201 Created
  - `category_id` auto-saved
- [ ] Get category details → Expected: 200 OK
- [ ] Update category (name/color) → Expected: 200 OK
- [ ] Delete category → Expected: 204 No Content
- [ ] Verify category removed from list

### Category Validation
- [ ] Create duplicate category (case-insensitive) → Expected: 400 Bad Request
- [ ] Create category with invalid color → Expected: 400 Bad Request
- [ ] Create category with empty name → Expected: 400 Bad Request

### Category Panel Isolation
- [ ] Panel A categories visible only in Panel A → Expected: true
- [ ] Panel B has separate categories → Expected: true

---

## Phase 5: Expenses

### Expense CRUD
- [ ] Create expense
  - Amount: `50.00`
  - Category: `{{category_id}}`
  - Panel: `{{panel_id}}`
  - Date: `2026-05-04`
  - Description: `Lunch`
  - Expected: 201 Created
  - `expense_id` auto-saved
- [ ] List expenses → Expected: 200 OK, returns array
- [ ] Get expense details → Expected: 200 OK
- [ ] Update expense (amount, description) → Expected: 200 OK
- [ ] Delete expense (soft-delete) → Expected: 204 No Content
- [ ] List expenses (deleted not shown) → Expected: expense removed from list
- [ ] Restore expense (if available) → Expected: 200 OK

### Expense Validation
- [ ] Create with negative amount → Expected: 400 Bad Request
- [ ] Create with null category → Expected: 400 Bad Request
- [ ] Create with future date → Expected: 201 OK (allowed)
- [ ] Update with invalid category → Expected: 400 Bad Request

### Expenses by Category
- [ ] Create 3 expenses in different categories
- [ ] GET `/expenses/by_category/` → Expected: 200 OK, grouped by category
- [ ] Verify totals accurate

### Expense Permissions
- [ ] Owner creates expense → Expected: 201 OK
- [ ] Editor creates expense → Expected: 201 OK
- [ ] Viewer creates expense → Expected: 403 Forbidden
- [ ] Non-member creates expense → Expected: 403 Forbidden

### Batch Operations
- [ ] Create 10 expenses with pagination
- [ ] List first page → Expected: entries 1-10
- [ ] List second page → Expected: entries 11+

---

## Phase 6: Budgets

### Budget CRUD
- [ ] Create budget
  - Amount: `500.00`
  - Category: `{{category_id}}`
  - Period: `monthly`
  - Start: `2026-05-01`
  - End: `2026-05-31`
  - Alert threshold: `80`
  - Expected: 201 Created
  - `budget_id` auto-saved
- [ ] List budgets → Expected: 200 OK
- [ ] Get budget → Expected: 200 OK
- [ ] Update budget (amount, threshold) → Expected: 200 OK
- [ ] Delete budget → Expected: 204 No Content

### Budget Validation
- [ ] Create with negative amount → Expected: 400 Bad Request
- [ ] Create with end_date < start_date → Expected: 400 Bad Request
- [ ] Create with invalid threshold (>100) → Expected: 400 Bad Request
- [ ] Create with invalid period → Expected: 400 Bad Request

### Budget Monitoring
- [ ] Create budget for `$500/month` on `2026-05-01 to 2026-05-31`
- [ ] Create 3 expenses totaling `$420`
- [ ] GET `/budgets/check_status/` → Expected: 200 OK, shows 84% spent
- [ ] Verify remaining: `$80`
- [ ] Create expense exceeding budget → Expected: notification triggered
- [ ] Check notifications → Expected: "Budget exceeded" notification

### Budget Alerts
- [ ] Set alert threshold to `80%`
- [ ] Create expenses = `80.1%` of budget
- [ ] Expected: notification created with alert
- [ ] Verify notification includes budget name and percentage

---

## Phase 7: Reports & Analytics

### Report Summary
- [ ] GET `/reports/summary/?panel_id={{panel_id}}`
  - Expected: 200 OK
  - Returns: total_income, total_expenses, net_balance, by_category breakdown
- [ ] Verify totals match expenses created
- [ ] Response cached (check response time < 50ms on second call)

### Report Monthly
- [ ] GET `/reports/monthly/?panel_id={{panel_id}}&year=2026&month=5`
  - Expected: 200 OK
  - Returns: daily breakdown for May 2026
- [ ] Verify sum equals monthly total
- [ ] Try invalid month → Expected: 200 OK with empty/zero data

### Report Trends
- [ ] GET `/reports/trends/?panel_id={{panel_id}}`
  - Expected: 200 OK
  - Returns: category breakdown, totals by category
- [ ] Verify all categories represented

### Export Formats

#### JSON Export
- [ ] GET `/reports/summary/?export=json`
  - Expected: 200 OK, Content-Type: application/json
  - Data in JSON format

#### CSV Export
- [ ] GET `/reports/summary/?export=csv`
  - Expected: 200 OK, Content-Type: text/csv
  - Download as .csv file
  - Open in Excel to verify format

#### XLSX Export
- [ ] GET `/reports/summary/?export=xlsx`
  - Expected: 200 OK, Content-Type: application/vnd.ms-excel
  - Download as .xlsx file
  - Open in Excel to verify formatting

#### PDF Export
- [ ] GET `/reports/summary/?export=pdf`
  - Expected: 200 OK, Content-Type: application/pdf
  - Download as .pdf file
  - Open in PDF viewer

### Export with Date Filtering
- [ ] GET `/reports/summary/?export=csv&date_from=2026-05-01&date_to=2026-05-31`
  - Expected: 200 OK
  - Verify dates in range only
- [ ] Try invalid date format → Expected: 400 Bad Request

### Report Caching
- [ ] Call `/reports/summary/` twice within 5 minutes
  - Expected: Second call much faster (cached)
- [ ] Check X-Cache header if available
- [ ] Wait 5 minutes, call again → Expected: fresh data

---

## Phase 8: Recurring Expenses

### Recurring Expense CRUD
- [ ] Create recurring expense
  - Name: `Monthly Rent`
  - Amount: `1500.00`
  - Category: `{{category_id}}`
  - Frequency: `monthly`
  - Start date: `2026-05-01`
  - Expected: 201 Created
  - `recurring_expense_id` auto-saved
- [ ] List recurring expenses → Expected: 200 OK
- [ ] Get recurring expense → Expected: 200 OK
- [ ] Update recurring expense → Expected: 200 OK
- [ ] Delete recurring expense → Expected: 204 No Content

### Recurring Frequency Support
- [ ] Create daily recurring
- [ ] Create weekly recurring
- [ ] Create bi-weekly recurring
- [ ] Create monthly recurring
- [ ] Create quarterly recurring
- [ ] Create yearly recurring
- [ ] All expected: 201 Created

### Recurring Validation
- [ ] Create with invalid frequency → Expected: 400 Bad Request
- [ ] Create with null amount → Expected: 400 Bad Request
- [ ] Create with end_date < start_date → Expected: 400 Bad Request

### Auto-Generation (Manual Trigger)
- [ ] Create monthly recurring on 2026-05-01
- [ ] Manually trigger background task (if available)
- [ ] Check new expense auto-created
- [ ] Verify amount and category match
- [ ] Verify date = next scheduled occurrence

---

## Phase 9: Webhooks

### Webhook CRUD
- [ ] Create webhook
  - URL: `https://webhook.site/<unique-id>`
  - Event: `expense.created`
  - Expected: 201 Created, `webhook_id` and secret returned
  - `webhook_id` auto-saved
  - `webhook_secret` auto-saved
- [ ] List webhooks → Expected: 200 OK
- [ ] Get webhook → Expected: 200 OK, includes secret
- [ ] Update webhook (URL, event) → Expected: 200 OK
- [ ] Delete webhook → Expected: 204 No Content

### Webhook Event Subscriptions
- [ ] Subscribe to `expense.created` event
- [ ] Subscribe to `expense.updated` event
- [ ] Subscribe to `expense.deleted` event
- [ ] Subscribe to `budget.exceeded` event
- [ ] Subscribe to `panel.invitation` event
- [ ] Subscribe to `report.run` event

### Webhook Testing
- [ ] Create webhook with webhook.site URL
- [ ] GET `/webhooks/{{webhook_id}}/test_send/`
  - Expected: 200 OK
  - Check webhook.site - verify delivery received
  - Verify signature in headers

### Webhook Delivery on Events
- [ ] Create webhook for `expense.created`
- [ ] Create new expense
- [ ] Check webhook.site → Expected: delivery received
- [ ] Verify payload includes expense data
- [ ] Verify HMAC-SHA256 signature in headers

### Webhook Payload Validation
- [ ] Create expense via API
- [ ] Webhook received contains:
  - [ ] `event`: `"expense.created"`
  - [ ] `timestamp`: ISO timestamp
  - [ ] `data.id`: expense ID
  - [ ] `data.amount`: expense amount
  - [ ] `data.category`: category name
  - [ ] `data.description`: description

### Webhook Signature Verification
- [ ] Extract `X-Webhook-Signature` header
- [ ] Extract webhook secret
- [ ] Compute HMAC-SHA256(secret, body)
- [ ] Verify computed signature matches header

---

## Phase 10: Scheduled Reports

### Report Schedule CRUD
- [ ] Create schedule
  - Name: `Weekly Report`
  - Frequency: `weekly`
  - Day: `monday`
  - Format: `pdf`
  - Recipients: `admin@example.com`
  - Expected: 201 Created
  - `schedule_id` auto-saved
- [ ] List schedules → Expected: 200 OK
- [ ] Get schedule → Expected: 200 OK
- [ ] Update schedule → Expected: 200 OK
- [ ] Delete schedule → Expected: 204 No Content

### Schedule Frequencies
- [ ] Create daily schedule
- [ ] Create weekly schedule (specify day)
- [ ] Create monthly schedule (specify day of month)
- [ ] All expected: 201 Created

### Manual Execution
- [ ] Create schedule with future next_run_at
- [ ] POST `/report-schedules/{{schedule_id}}/run_now/`
  - Expected: 200 OK
  - Report generated immediately
  - Webhook triggered with `report.run` event
  - Notification created for user

### Auto-Execution (Celery Beat)
- [ ] Create schedule with past next_run_at (e.g., 1 hour ago)
- [ ] Wait for Celery beat (every 5 min check)
- [ ] Expected: report auto-executed
- [ ] Expected: next_run_at advanced
- [ ] Check notifications → Expected: delivery receipt

---

## Phase 11: Notifications

### Notification CRUD
- [ ] Create expense (triggers notification)
  - Expected: notification created if above category threshold
- [ ] List notifications → Expected: 200 OK, returns array
- [ ] Get notification → Expected: 200 OK
- [ ] Get unread notifications → Expected: 200 OK, only unread items
- [ ] Mark single notification read
  - Expected: 200 OK
  - `is_read` becomes `true`
- [ ] Mark all notifications read
  - Expected: 200 OK
  - All notifications marked read

### Notification Types
- [ ] Budget alert notification
- [ ] Budget exceeded notification
- [ ] Invitation received notification
- [ ] Report scheduled notification
- [ ] Webhook delivery confirmation notification

### Notification Preferences
- [ ] List preferences → Expected: 200 OK
- [ ] Get preference → Expected: 200 OK
- [ ] Update preference (enable/disable notifications)
  - Expected: 200 OK
- [ ] Disable budget alerts
- [ ] Create expense → Expected: no notification
- [ ] Re-enable → Create expense → Expected: notification

---

## Phase 12: Audit Logging

### Audit Trail
- [ ] List audit logs → Expected: 200 OK
- [ ] Get audit log → Expected: 200 OK
- [ ] Verify logs are read-only (no update/delete)

### Audit Events Captured
- [ ] User registration → Expected: audit entry created
- [ ] User login → Expected: audit entry created
- [ ] User logout → Expected: audit entry created
- [ ] Panel created → Expected: audit entry created
- [ ] Panel updated → Expected: audit entry created
- [ ] Panel deleted → Expected: audit entry created
- [ ] Expense created → Expected: audit entry created
- [ ] Expense updated → Expected: audit entry created
- [ ] Expense deleted → Expected: audit entry created
- [ ] Budget created → Expected: audit entry created
- [ ] Role changed → Expected: audit entry created
- [ ] Invitation sent → Expected: audit entry created
- [ ] Invitation accepted → Expected: audit entry created

### Audit Log Content
- [ ] Verify includes:
  - [ ] `actor`: user who performed action
  - [ ] `action`: type of action (create/update/delete)
  - [ ] `entity_type`: what entity (expense/budget/etc)
  - [ ] `entity_id`: ID of entity
  - [ ] `description`: human-readable description
  - [ ] `timestamp`: when action occurred
  - [ ] `ip_address`: client IP
  - [ ] `user_agent`: browser info
  - [ ] `metadata`: additional context (old values, new values, etc)

### Multi-user Audit Trail
- [ ] User A performs action
- [ ] Check audit log → action attributed to User A
- [ ] User B performs action
- [ ] Check audit log → separate entries for each user
- [ ] Verify isolation between users

---

## Phase 13: Rate Limiting

### Anonymous User Limits
- [ ] Anonymous user: 100 requests/hour limit
- [ ] Make 101 requests rapidly
  - Expected: 100 succeed, 101st returns 429 Too Many Requests
- [ ] Wait until limit resets or use different IP

### Authenticated User Limits
- [ ] Authenticated user: 1000 requests/hour limit
- [ ] Make 1001 requests
  - Expected: 1000 succeed, 1001st returns 429
- [ ] Response includes `Retry-After` header

### Rate Limit Headers
- [ ] Check response headers:
  - [ ] `X-RateLimit-Limit`: total requests allowed
  - [ ] `X-RateLimit-Remaining`: requests left
  - [ ] `X-RateLimit-Reset`: when limit resets (Unix timestamp)

---

## Phase 14: Error Handling

### 400 Bad Request
- [ ] Send invalid JSON → Expected: 400 Bad Request
- [ ] Send missing required fields → Expected: 400 Bad Request
- [ ] Send invalid data type → Expected: 400 Bad Request
- [ ] Verify error message helpful

### 401 Unauthorized
- [ ] No token provided → Expected: 401 Unauthorized
- [ ] Expired token → Expected: 401 Unauthorized
- [ ] Invalid token format → Expected: 401 Unauthorized
- [ ] Blacklisted token → Expected: 401 Unauthorized

### 403 Forbidden
- [ ] Access other user's panel → Expected: 403 Forbidden
- [ ] Viewer tries to create expense → Expected: 403 Forbidden
- [ ] Non-member accesses panel → Expected: 403 Forbidden

### 404 Not Found
- [ ] GET non-existent expense → Expected: 404 Not Found
- [ ] GET non-existent panel → Expected: 404 Not Found
- [ ] GET non-existent category → Expected: 404 Not Found

### 429 Too Many Requests
- [ ] Exceed rate limit → Expected: 429 Too Many Requests
- [ ] Verify retry-after header included

### 500 Internal Server Error
- [ ] Trigger server error (if applicable)
- [ ] Check Django logs for details
- [ ] Verify error response is generic (no sensitive info leaked)

---

## Phase 15: Data Validation

### Email Validation
- [ ] Register with invalid email format → Expected: 400 Bad Request
- [ ] Invite with invalid email → Expected: 400 Bad Request
- [ ] Valid emails accepted

### Date Validation
- [ ] Create expense with invalid date format → Expected: 400 Bad Request
- [ ] Create budget with end_date < start_date → Expected: 400 Bad Request
- [ ] Create with valid date → Expected: 201 Created

### Numeric Validation
- [ ] Create expense with negative amount → Expected: 400 Bad Request
- [ ] Create expense with amount=0 → Expected: 400 Bad Request
- [ ] Create expense with decimal amount → Expected: 201 Created
- [ ] Create budget with invalid threshold (>100) → Expected: 400 Bad Request

### Enum Validation
- [ ] Create recurring with invalid frequency → Expected: 400 Bad Request
- [ ] Create budget with invalid period → Expected: 400 Bad Request
- [ ] Create schedule with invalid day → Expected: 400 Bad Request
- [ ] Invite with invalid role → Expected: 400 Bad Request

### String Validation
- [ ] Create category with empty name → Expected: 400 Bad Request
- [ ] Create panel with name > 200 chars → Expected: 400 Bad Request
- [ ] Special characters in strings → Expected: 201 Created (accepted)

---

## Phase 16: Concurrency & Edge Cases

### Concurrent Requests
- [ ] Create 10 expenses simultaneously
- [ ] Expected: all succeed without conflicts
- [ ] Verify all expenses recorded correctly
- [ ] Totals accurate

### Double-spend Prevention
- [ ] Create budget $500, threshold 100%
- [ ] Create expense $500
- [ ] Create expense $1 simultaneously
  - Expected: one succeeds, one fails OR both succeed with notification
  - Verify total >= $501 (no data loss)

### Idempotency
- [ ] Send same creation request twice
- [ ] Expected: first succeeds, second fails OR same resource returned
- [ ] No duplicate resources created

### Cascade Operations
- [ ] Delete panel with expenses
  - Expected: 204 No Content
  - Expenses also deleted (cascade or soft delete handled)
- [ ] Delete category with expenses
  - Expected: 400 Bad Request (prevent orphaned expenses) OR category marked deleted

### Timezone Handling
- [ ] Create expense with timezone-aware timestamp
- [ ] Expected: stored correctly
- [ ] Retrieved with correct timezone

---

## Final Validation Checklist

### Security
- [ ] [ ] All endpoints require authentication (except register/login)
- [ ] [ ] JWT tokens validated on every request
- [ ] [ ] Role-based access enforced
- [ ] [ ] Panel isolation verified
- [ ] [ ] Webhook signatures validated
- [ ] [ ] No sensitive data in logs
- [ ] [ ] No SQL injection vulnerabilities
- [ ] [ ] No XSS vulnerabilities
- [ ] [ ] CORS properly configured

### Performance
- [ ] [ ] Report endpoints respond < 500ms
- [ ] [ ] List endpoints paginated and sorted
- [ ] [ ] Cache working (repeated calls faster)
- [ ] [ ] No N+1 query problems
- [ ] [ ] Database indexes in place

### Reliability
- [ ] [ ] All 27 tests pass
- [ ] [ ] No warnings in migrations
- [ ] [ ] System checks pass
- [ ] [ ] Error messages helpful
- [ ] [ ] Graceful degradation when optional services unavailable

### Documentation
- [ ] [ ] Postman collection complete
- [ ] [ ] All endpoints documented
- [ ] [ ] Swagger UI accessible
- [ ] [ ] README accurate
- [ ] [ ] Examples provided

---

## Test Summary

| Category | Tests | Status |
|----------|-------|--------|
| Authentication | 15 | [ ] Pass |
| Panels | 20 | [ ] Pass |
| Invitations | 12 | [ ] Pass |
| Expenses | 25 | [ ] Pass |
| Budgets | 18 | [ ] Pass |
| Reports | 15 | [ ] Pass |
| Recurring | 10 | [ ] Pass |
| Webhooks | 12 | [ ] Pass |
| Schedules | 10 | [ ] Pass |
| Notifications | 10 | [ ] Pass |
| Audit | 8 | [ ] Pass |
| Rate Limiting | 5 | [ ] Pass |
| Error Handling | 8 | [ ] Pass |
| Validation | 12 | [ ] Pass |
| Concurrency | 5 | [ ] Pass |
| **TOTAL** | **182** | **[ ] Pass** |

---

**Estimated Time**: 2-3 hours for complete test suite

**Date Completed**: _______________

**Tester Name**: _______________

**Notes**: 
