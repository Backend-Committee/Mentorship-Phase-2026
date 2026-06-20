# PMS API Endpoints

## 🔐 Accounts App API Endpoints

This module handles user authentication, registration, and user management. All standard endpoints are prefixed with `/api/accounts/`.

### Authentication Endpoints
| HTTP Method | Endpoint | Description | Auth Required | Body/Payload |
|-------------|----------|-------------|---------------|--------------|
| `POST` | `/api/accounts/login/` | Get JWT access and refresh tokens. | No | `{"username": "...", "password": "..."}` |
| `POST` | `/api/accounts/token/refresh/` | Get a new access token using a refresh token. | No | `{"refresh": "..."}` |

### Users Management Endpoints (CRUD)
| HTTP Method | Endpoint | Description | Permissions | Body/Payload |
|-------------|----------|-------------|-------------|--------------|
| `GET` | `/api/accounts/users/` | List all users. | Manager Only | - |
| `POST` | `/api/accounts/users/` | Create a new user. | Manager Only | `{"username": "...", "password": "...", "phone": "..."}`* |
| `GET` | `/api/accounts/users/{id}/` | Retrieve a specific user's details. | Authenticated | - |
| `PUT / PATCH` | `/api/accounts/users/{id}/` | Update a specific user's details. | Authenticated | User fields |
| `DELETE` | `/api/accounts/users/{id}/` | Delete a user. | Manager Only | - |

### Custom User Actions
| HTTP Method | Endpoint | Description | Permissions | Body/Payload |
|-------------|----------|-------------|-------------|--------------|
| `GET` | `/api/accounts/users/me/` | Get the profile details of the currently logged-in user. | Authenticated | - |
| `POST` | `/api/accounts/users/change-password/` | Change the password for the current logged-in user. | Authenticated | `{"password": "new_password"}` |

> **📝 Notes on the User Payload:**
> * `password`: Write-only field.
> * `id`, `hourly_rate`, `hours`: Read-only fields (cannot be set manually).
> * `phone`: Must be exactly 11 digits and start with a valid Egyptian prefix (`010`, `011`, `012`, `015`).

## 📦 Inventory App API Endpoints

This module manages the pharmacy's stock, including medicines and reported shortages. All standard endpoints are prefixed with `/api/inventory/`.

### 💊 Medicines Management Endpoints (CRUD & Filter)
| HTTP Method | Endpoint | Description | Permissions / Rules | Body/Payload |
|-------------|----------|-------------|---------------------|--------------|
| `GET` | `/api/inventory/medicines/` | List all medicines. Supports searching by `name` or `barcode`, and filtering by `type`. | Authenticated | - |
| `POST` | `/api/inventory/medicines/` | Add a new medicine to the stock. | Authenticated | `{"name": "...", "barcode": "...", "price": 10.5, "stock_quantity": 100, "min_stock": 10, "type": "..."}` |
| `GET` | `/api/inventory/medicines/{id}/` | Retrieve a specific medicine's details. | Authenticated | - |
| `PUT / PATCH` | `/api/inventory/medicines/{id}/` | Update a specific medicine. | **Non-Managers cannot decrease** the `stock_quantity` manually. | Medicine fields |
| `DELETE` | `/api/inventory/medicines/{id}/` | Delete a medicine from the database. | **Manager Only** | - |

#### 🔍 Custom Medicine Actions
| HTTP Method | Endpoint | Description | Permissions | Body/Payload |
|-------------|----------|-------------|-------------|--------------|
| `GET` | `/api/inventory/medicines/low_stock/` | Retrieve a list of all medicines where `stock_quantity` is less than or equal to `min_stock`. | Authenticated | - |


### ⚠️ Shortages Management Endpoints (CRUD)
| HTTP Method | Endpoint | Description | Permissions / Rules | Body/Payload |
|-------------|----------|-------------|---------------------|--------------|
| `GET` | `/api/inventory/shortages/` | List all reported shortages ordered by reporting date. | Authenticated | - |
| `POST` | `/api/inventory/shortages/` | Report a missing or low-stock medicine. | Authenticated | `{"medicine": id, "quantity_needed": 5}` or `{"medicine_name": "...", "quantity_needed": 5}` |
| `GET` | `/api/inventory/shortages/{id}/` | Retrieve specific shortage details. | Authenticated | - |
| `PUT / PATCH` | `/api/inventory/shortages/{id}/` | Update shortage status (e.g., marking as ordered). | **Only Manager** can set `is_ordered` to `True`. | Shortage fields |
| `DELETE` | `/api/inventory/shortages/{id}/` | Remove a shortage record. | Authenticated | - |

> **📝 Business Logic Notes:**
> * **Medicines Validation:** Fields `price`, `stock_quantity`, and `min_stock` cannot accept negative values.
> * **Shortages Autocomplete:** When creating a shortage, if you provide a `medicine` ID, the backend automatically extracts and fills the `medicine_name` for you. If no ID is passed, `medicine_name` becomes mandatory.

## 🏪 Shifts & Expenses App API Endpoints

This module manages daily cashier shifts, starting/closing cash, and shift-related expenses. All standard endpoints are prefixed with `/api/shifts/`.

### ⏱️ Shifts Management Endpoints (CRUD)
| HTTP Method | Endpoint | Description | Permissions | Body/Payload |
|-------------|----------|-------------|-------------|--------------|
| `GET` | `/api/shifts/` | List all shifts. | **Manager Only** | - |
| `POST` | `/api/shifts/` | Open a new shift. Automatically linked to the logged-in user. | Authenticated | `{"starting_cash": 1000}` |
| `GET` | `/api/shifts/{id}/` | Retrieve a specific shift's details (includes calculated sales, expenses, and expected cash). | Authenticated | - |
| `PUT / PATCH` | `/api/shifts/{id}/` | Update shift details. | Authenticated | Shift fields |
| `DELETE` | `/api/shifts/{id}/` | Delete a shift record. | **Manager Only** | - |

#### 🔒 Custom Shift Actions
| HTTP Method | Endpoint | Description | Permissions | Body/Payload |
|-------------|----------|-------------|-------------|--------------|
| `POST` | `/api/shifts/{id}/close_shift/` | Close an active shift and calculate differences (shortage/surplus). | Authenticated | `{"closing_cash": 1500}` |


### 💸 Expenses Management Endpoints (CRUD)
| HTTP Method | Endpoint | Description | Permissions | Body/Payload |
|-------------|----------|-------------|-------------|--------------|
| `GET` | `/api/shifts/expenses/` | List all recorded expenses. | Authenticated | - |
| `POST` | `/api/shifts/expenses/` | Add a new expense. Automatically linked to the currently **Active Shift**. | Authenticated | `{"amount": 150.00, "description": "cleaning tools"}` |
| `GET` | `/api/shifts/expenses/{id}/` | Retrieve specific expense details. | Authenticated | - |
| `PUT / PATCH` | `/api/shifts/expenses/{id}/` | Update an expense. | Authenticated | Expense fields |
| `DELETE` | `/api/shifts/expenses/{id}/` | Remove an expense. | Authenticated | - |

> **📝 Business Logic Notes:**
> * **Active Shift Rule:** Only one active (open) shift can exist at a time. The system will reject opening a new shift if there is an existing unclosed shift.
> * **Automated Calculations:** `total_sales`, `total_expenses`, `total_debt_payments`, `expected_cash`, and `difference` are calculated dynamically on the fly and are **Read-Only**.
> * **Expenses Linking:** When creating an expense, you **do not** need to send the `shift` ID. The system automatically fetches the currently open shift and links the expense to it.

## 🛒 Sales & Invoices App API Endpoints

This module handles all sales operations, invoice generation, returns, and automatic stock/debt adjustments. All standard endpoints are prefixed with `/api/sales/`.

### 🧾 Invoices Management Endpoints
| HTTP Method | Endpoint | Description | Permissions | Body/Payload |
|-------------|----------|-------------|-------------|--------------|
| `GET` | `/api/sales/invoices/` | List all invoices (Sales and Returns). | Authenticated | - |
| `POST` | `/api/sales/invoices/` | Create a new invoice. Automatically linked to the active shift, calculates total price, and updates medicine stock. | Authenticated | *See nested payload below* |
| `GET` | `/api/sales/invoices/{id}/` | Retrieve specific invoice details along with its items. | Authenticated | - |
| `PUT / PATCH` | `/api/sales/invoices/{id}/` | Update basic invoice details (though usually restricted due to accounting rules). | Authenticated | Invoice fields |
| `DELETE` | `/api/sales/invoices/{id}/` | **Void/Cancel an invoice.** Soft deletes the invoice (`is_valid=False`), restores medicine stock, and reverts customer debt. | **Manager** (if shift closed) | - |

> **💡 Note on Creating an Invoice (Nested Payload):**
> When creating an invoice, you must pass the items inside the same request. You do not need to send `shift`, `total_price`, or `is_valid` as they are calculated automatically.
> ```json
> {
>     "type": "Sale",             // "Sale" or "Return"
>     "payment_method": "Cash",   // "Cash" or "Debt"
>     "customer": 1,              // Required ONLY if payment_method is "Debt"
>     "items": [
>         {
>             "medicine": 3,
>             "quantity": 2,
>             "unit_price": 50.50
>         }
>     ]
> }
> ```

### 💊 Invoice Items Endpoints (Read-Only)
| HTTP Method | Endpoint | Description | Permissions | Body/Payload |
|-------------|----------|-------------|-------------|--------------|
| `GET` | `/api/sales/invoice-items/` | List all individual items sold/returned across all invoices. | Authenticated | - |
| `GET` | `/api/sales/invoice-items/{id}/` | Retrieve details of a specific invoice item. | Authenticated | - |

> **📝 Business Logic & Validation Notes:**
> * **Active Shift Requirement:** An invoice cannot be created unless there is an actively open shift.
> * **Stock Validation:** The system will reject a `Sale` invoice if the requested `quantity` exceeds the available `stock_quantity` for any medicine.
> * **Debt Validation:** If `payment_method` is set to `Debt`, linking a `customer` is strictly required.
> * **Voiding Restrictions:** You cannot cancel/delete an invoice that is already a `Return` type. If the shift is closed, only users with a `Manager` role can void invoices.

## 👥 Customer & Debt Management App API Endpoints

This module manages customer profiles, tracks credit/debts, and records debt payments which automatically affect the active shift's cash. All standard endpoints are prefixed with your base app route (e.g., `/api/debts/`).

### 👤 Customers Management Endpoints (CRUD)
| HTTP Method | Endpoint | Description | Permissions / Rules | Body/Payload |
|-------------|----------|-------------|---------------------|--------------|
| `GET` | `/api/debts/customers/` | List all customers ordered by their total debt (highest first). | Authenticated | - |
| `POST` | `/api/debts/customers/` | Register a new customer. | Authenticated | `{"name": "...", "phone": "..."}` |
| `GET` | `/api/debts/customers/{id}/` | Retrieve specific customer details. | Authenticated | - |
| `PUT / PATCH` | `/api/debts/customers/{id}/` | Update customer details. | **Only Manager** can manually edit `total_debt`. | Customer fields |
| `DELETE` | `/api/debts/customers/{id}/` | Delete a customer profile. | **Manager Only** | - |

### 📉 Customer Debts Endpoints (Detailed Tracking)
| HTTP Method | Endpoint | Description | Permissions | Body/Payload |
|-------------|----------|-------------|-------------|--------------|
| `GET` | `/api/debts/customer-debts/` | List detailed debt records. | Authenticated | - |
| `POST` | `/api/debts/customer-debts/` | Create a manual debt record. | Authenticated | `{"customer": id, "amount": 500}` |
| `PUT / PATCH` | `/api/debts/customer-debts/{id}/` | Update a detailed debt record. | **Manager Only** | Debt fields |
| `DELETE` | `/api/debts/customer-debts/{id}/` | Delete a detailed debt record. | **Manager Only** | - |

### 💵 Debt Payments Endpoints
| HTTP Method | Endpoint | Description | Permissions / Rules | Body/Payload |
|-------------|----------|-------------|---------------------|--------------|
| `GET` | `/api/debts/debt-payments/` | List all recorded payments ordered by the latest date. | Authenticated | - |
| `POST` | `/api/debts/debt-payments/` | Record a new payment from a customer. Automatically updates customer's `total_debt` and adds to the active shift's `total_debt_payments`. | Authenticated | `{"customer": 1, "amount": 200}` |
| `GET` | `/api/debts/debt-payments/{id}/` | Retrieve specific payment details. | Authenticated | - |

> **📝 Business Logic & Validation Notes:**
> * **Active Shift Requirement:** You cannot record a customer `Debt Payment` unless there is an actively open shift.
> * **Payment Amount Restriction:** The system will validate and reject any payment `amount` that is greater than the customer's current `total_debt`.
> * **Phone Validation:** Customer phone numbers must be exactly 11 digits and strictly comprised of numbers.