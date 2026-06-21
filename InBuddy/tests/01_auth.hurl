# Authentication Tests
# Tests for registration, login, token refresh, and token verification

# --- Register a new user ---
POST {{base_url}}/api/auth/users/
Content-Type: application/json

{
  "email": "hurltest@example.com",
  "username": "hurltestuser",
  "password": "TestPass123!",
  "first_name": "Hurl",
  "last_name": "Tester"
}

HTTP 201
[Captures]
user_id: jsonpath "$.id"
created_email: jsonpath "$.email"

[Asserts]
assert jsonpath "$.id" != null
assert jsonpath "$.email" == "hurltest@example.com"
assert jsonpath "$.username" == "hurltestuser"
assert jsonpath "$.first_name" == "Hurl"
assert jsonpath "$.last_name" == "Tester"

---

# --- Login with registered user ---
POST {{base_url}}/api/auth/jwt/create/
Content-Type: application/json

{
  "email": "hurltest@example.com",
  "password": "TestPass123!"
}

HTTP 200
[Captures]
access_token: jsonpath "$.access"
refresh_token: jsonpath "$.refresh"

[Asserts]
assert jsonpath "$.access" != null
assert jsonpath "$.refresh" != null

---

# --- Refresh access token ---
POST {{base_url}}/api/auth/jwt/refresh/
Content-Type: application/json

{
  "refresh": "{{refresh_token}}"
}

HTTP 200
[Captures]
new_access_token: jsonpath "$.access"
new_refresh_token: jsonpath "$.refresh"

[Asserts]
assert jsonpath "$.access" != null
assert jsonpath "$.refresh" != null

---

# --- Verify access token ---
POST {{base_url}}/api/auth/jwt/verify/
Content-Type: application/json

{
  "token": "{{access_token}}"
}

HTTP 200

---

# --- Verify invalid token (should fail) ---
POST {{base_url}}/api/auth/jwt/verify/
Content-Type: application/json

{
  "token": "invalid.token.here"
}

HTTP 401

---

# --- Login with invalid credentials (should fail) ---
POST {{base_url}}/api/auth/jwt/create/
Content-Type: application/json

{
  "email": "hurltest@example.com",
  "password": "WrongPassword!"
}

HTTP 401

---

# --- Register duplicate user (should fail) ---
POST {{base_url}}/api/auth/users/
Content-Type: application/json

{
  "email": "hurltest@example.com",
  "username": "hurltestuser",
  "password": "TestPass123!"
}

HTTP 400
