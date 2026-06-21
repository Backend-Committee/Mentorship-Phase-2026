# User Profile Tests
# Tests for getting, updating, and deleting user profile
# Requires: 01_auth.hurl to run first (for access_token and user_id)

# --- Get current user profile ---
GET {{base_url}}/api/users/profile/
Authorization: Bearer {{access_token}}

HTTP 200
[Asserts]
assert jsonpath "$.id" == user_id
assert jsonpath "$.email" == "hurltest@example.com"
assert jsonpath "$.username" == "hurltestuser"
assert jsonpath "$.first_name" == "Hurl"
assert jsonpath "$.last_name" == "Tester"

---

# --- Update user profile (PATCH) ---
PATCH {{base_url}}/api/users/profile/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "first_name": "Updated",
  "last_name": "Name",
  "age": 25,
  "gender": "male",
  "height_cm": 175.5,
  "weight_kg": 70.0,
  "goal": "gain_muscle",
  "activity_level": "moderate"
}

HTTP 200
[Captures]
updated_first_name: jsonpath "$.first_name"
updated_last_name: jsonpath "$.last_name"
updated_age: jsonpath "$.age"
updated_gender: jsonpath "$.gender"
updated_height: jsonpath "$.height_cm"
updated_weight: jsonpath "$.weight_kg"
updated_goal: jsonpath "$.goal"
updated_activity: jsonpath "$.activity_level"

[Asserts]
assert jsonpath "$.first_name" == "Updated"
assert jsonpath "$.last_name" == "Name"
assert jsonpath "$.age" == 25
assert jsonpath "$.gender" == "male"
assert jsonpath "$.height_cm" == 175.5
assert jsonpath "$.weight_kg" == 70.0
assert jsonpath "$.goal" == "gain_muscle"
assert jsonpath "$.activity_level" == "moderate"

---

# --- Verify profile was updated ---
GET {{base_url}}/api/users/profile/
Authorization: Bearer {{access_token}}

HTTP 200
[Asserts]
assert jsonpath "$.first_name" == "Updated"
assert jsonpath "$.last_name" == "Name"
assert jsonpath "$.age" == 25
assert jsonpath "$.gender" == "male"
assert jsonpath "$.height_cm" == 175.5
assert jsonpath "$.weight_kg" == 70.0
assert jsonpath "$.goal" == "gain_muscle"
assert jsonpath "$.activity_level" == "moderate"

---

# --- Get profile without auth (should fail) ---
GET {{base_url}}/api/users/profile/

HTTP 401
