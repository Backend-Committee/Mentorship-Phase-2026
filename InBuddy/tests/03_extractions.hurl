# Text Extraction Tests
# Tests for creating, listing, getting, and deleting extraction tasks
# Requires: 01_auth.hurl to run first (for access_token)

# --- List extractions (empty initially) ---
GET {{base_url}}/api/extractions/
Authorization: Bearer {{access_token}}

HTTP 200
[Asserts]
assert jsonpath "$.count" >= 0
assert exists jsonpath "$.results"

---

# --- Create extraction task (upload image) ---
POST {{base_url}}/api/extractions/
Authorization: Bearer {{access_token}}

[MultiPart]
image: file, "../InBuddy-Initial-Version/inbuddy/assets/inbody1.jpg"

HTTP 201
[Captures]
extraction_id: jsonpath "$.id"
extraction_status: jsonpath "$.status"
extraction_text: jsonpath "$.extracted_text"
extraction_image_url: jsonpath "$.image"

[Asserts]
assert jsonpath "$.id" != null
assert jsonpath "$.status" == "completed"
assert jsonpath "$.extracted_text" != null
assert jsonpath "$.image" != null

---

# --- Get extraction task by ID ---
GET {{base_url}}/api/extractions/{{extraction_id}}/
Authorization: Bearer {{access_token}}

HTTP 200
[Asserts]
assert jsonpath "$.id" == extraction_id
assert jsonpath "$.status" == "completed"
assert jsonpath "$.extracted_text" != null

---

# --- List extractions (should have one now) ---
GET {{base_url}}/api/extractions/
Authorization: Bearer {{access_token}}

HTTP 200
[Asserts]
assert jsonpath "$.count" >= 1
assert jsonpath "$.results[0].id" == extraction_id

---

# --- Get extraction without auth (should fail) ---
GET {{base_url}}/api/extractions/{{extraction_id}}/

HTTP 401

---

# --- Get non-existent extraction (should fail) ---
GET {{base_url}}/api/extractions/99999/
Authorization: Bearer {{access_token}}

HTTP 404

---

# --- Delete extraction task ---
DELETE {{base_url}}/api/extractions/{{extraction_id}}/
Authorization: Bearer {{access_token}}

HTTP 204

---

# --- Verify extraction was deleted ---
GET {{base_url}}/api/extractions/{{extraction_id}}/
Authorization: Bearer {{access_token}}

HTTP 404
