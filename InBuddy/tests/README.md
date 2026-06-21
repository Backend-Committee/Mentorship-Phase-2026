# InBuddy API - Hurl Tests
# ========================
# Run all tests:
#   hurl --variables-file vars.env tests/*.hurl
#
# Run with a specific base URL:
#   hurl --variable base_url=http://localhost:8000 tests/*.hurl
#
# Prerequisites:
#   - Install hurl: https://hurl.dev/docs/installation.html
#   - Have the Django server running on localhost:8000 (or your target URL)
#
# Test files:
#   01_auth.hurl         - Authentication (register, login, refresh, verify)
#   02_users.hurl        - User profile (get, update, delete)
#   03_extractions.hurl  - Text extraction (list, create, get, delete)
#   04_analysis.hurl     - Analysis (list, create, get, delete)
#   05_measurements.hurl - Measurements (list, create, latest, get, update, delete)
#
# Variables:
#   base_url  - API base URL (default: http://localhost:8000)
