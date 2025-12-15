"""
ARCHITECTURE GUIDE - Library Management System
Separation of Concerns: Models, Business Logic, Formatting, and Views
"""

# ============================================================================
# ARCHITECTURE LAYERS
# ============================================================================

"""
┌─────────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION LAYER                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CLI Views          Web Views         GUI Views        Other Views      │
│  (cli_view.py)      (web_view.py)     (gui_view.py)    (extensible)     │
│                                                                         │
│  • BookView         • WebBookView     • GUIBookView     • Mobile API    │
│  • UserView         • WebUserView     • GUIUserView     • Desktop UI    │
│  • TransactionView  • WebTransactionView  • GUITransactionView          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                              ↓ Uses
┌─────────────────────────────────────────────────────────────────────────┐
│                      FORMATTING LAYER                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Formatters (formatters.py)                                             │
│                                                                         │
│  • BookFormatter.format_books()     → List[dict]                        │
│  • UserFormatter.format_users()     → List[dict]                        │
│  • TransactionFormatter.format_transactions() → List[dict]              │
│                                                                         │
│  Converts Model Objects → JSON-friendly Dictionaries                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                              ↓ Uses
┌─────────────────────────────────────────────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Managers:                                                              │
│  • BookManager         - Add, update, delete, search books              │
│  • UserManager         - Add, update, delete, activate/deactivate       │
│  • TransactionManager  - Borrow, return, track transactions             │
│                                                                         │
│  Controllers:                                                           │
│  • LibraryApp          - Application orchestrator                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                              ↓ Uses
┌─────────────────────────────────────────────────────────────────────────┐
│                      DATA LAYER (Models)                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  • BaseModel    - Base class with common attributes (id, timestamps)    │
│  • Book         - Represents a library book                             │
│  • User         - Represents a library member                           │
│  • Transaction  - Represents a borrow/return event                      │
│                                                                         │
│  FileStorage    - Persistence engine (JSON serialization)               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
"""

# ============================================================================
# BENEFITS OF THIS ARCHITECTURE
# ============================================================================

BENEFITS = """
1. SEPARATION OF CONCERNS
   • Models: Data structure and validation
   • Managers: Business logic and operations
   • Formatters: Data transformation
   • Views: Presentation and UI
   
   → Easy to test each layer independently
   → Easy to modify one layer without affecting others

2. REUSABILITY
   • Same managers work with CLI, Web, GUI, Mobile, etc.
   • Same formatters transform data for all UIs
   • All views use the same core logic
   
   → Code duplication is eliminated
   → Consistent behavior across all interfaces

3. SCALABILITY
   • Add new view layers without changing managers
   • Add new formatters for different output types
   • Add new managers for new features
   
   → Easy to grow the application
   → Each layer can be developed independently

4. MAINTAINABILITY
   • Changes to business logic don't affect UI
   • UI changes don't affect business logic
   • Clear dependencies between layers
   
   → Easier to debug and fix issues
   → Clearer code organization

5. TESTABILITY
   • Test managers without UI
   • Test formatters with mock data
   • Test views with sample data
   
   → Faster test execution
   → Better test coverage
"""

# ============================================================================
# FILE STRUCTURE
# ============================================================================

FILE_STRUCTURE = """
Library Management System/
│
├── models/                          # Data models and business logic
│   ├── __init__.py
│   ├── BaseModel.py                 # Base class for all models
│   ├── Book.py                      # Book model
│   ├── User.py                      # User model
│   ├── Transaction.py               # Transaction model
│   ├── BookManager.py               # Book operations manager
│   ├── UserManager.py               # User operations manager
│   ├── TransactionManager.py         # Transaction operations manager
│   └── engine/
│       ├── __init__.py
│       └── file_storage.py          # JSON persistence engine
│
├── views/                           # Presentation layer (multiple UI options)
│   ├── __init__.py
│   ├── formatters.py                # Data formatters
│   ├── cli_view.py                  # CLI/Terminal views
│   ├── web_view.py                  # Web/API views (JSON)
│   ├── gui_view.py                  # GUI/Desktop views
│   └── mobile_view.py               # Mobile views (future)
│
├── storage/                         # Data persistence
│   ├── books.json                   # Books data
│   ├── users.json                   # Users data
│   └── transactions.json            # Transactions data
│
├── APP.py                           # Main CLI application
├── test_refactored.py               # Refactoring tests
├── ARCHITECTURE.md              # Documentation
└── README.md                        # Documentation

"""

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

USAGE_EXAMPLES = """
=============================================================================
EXAMPLE 1: Using CLI View (Current Implementation)
=============================================================================

from models.engine.file_storage import FileStorage
from models.BookManager import BookManager
from views.cli_view import BookView

# Initialize
storage = FileStorage()
book_manager = BookManager(storage)
book_view = BookView()

# Add a book
book = book_manager.add_book("Python 101", "John Doe", "123-456", "2023-01-01", 5)

# Display books (using CLI view)
all_books = book_manager.get_all_books()
book_view.display_books(all_books)  # Pretty printed table


=============================================================================
EXAMPLE 2: Using Web View (REST API)
=============================================================================

from models.engine.file_storage import FileStorage
from models.BookManager import BookManager
from views.web_view import WebBookView

# Initialize
storage = FileStorage()
book_manager = BookManager(storage)
web_view = WebBookView()

# Add a book
book = book_manager.add_book("Python 101", "John Doe", "123-456", "2023-01-01", 5)

# Get books as JSON
all_books = book_manager.get_all_books()
json_response = web_view.get_books_json(all_books)
# Output: {"status": "success", "data": [...], "count": 1}


=============================================================================
EXAMPLE 3: Using GUI View (Tkinter/PyQt)
=============================================================================

from models.engine.file_storage import FileStorage
from models.BookManager import BookManager
from views.gui_view import GUIBookView

# Initialize
storage = FileStorage()
book_manager = BookManager(storage)
gui_view = GUIBookView()

# Add a book
book = book_manager.add_book("Python 101", "John Doe", "123-456", "2023-01-01", 5)

# Get books for table display
all_books = book_manager.get_all_books()
table_rows = gui_view.get_books_for_table(all_books)
# Output: [(id, title, author, isbn, available, total), ...]

# Populate GUI table
for row in table_rows:
    table.insert('end', row)


=============================================================================
EXAMPLE 4: Adding Custom View
=============================================================================

# Create views/mobile_view.py

from views.formatters import BookFormatter

class MobileBookView:
    \"\"\"View for mobile applications.\"\"\"
    
    @staticmethod
    def get_books_compact(books):
        \"\"\"Get compact book data for mobile.\"\"\"
        formatted = BookFormatter.format_books(books)
        return [{
            "id": b["id"],
            "title": b["title"],
            "available": b["available_copies"]
        } for b in formatted]

# Usage
from models.BookManager import BookManager
from views.mobile_view import MobileBookView

book_manager = BookManager(storage)
mobile_view = MobileBookView()

all_books = book_manager.get_all_books()
mobile_data = mobile_view.get_books_compact(all_books)
"""

# ============================================================================
# EXTENDING THE SYSTEM
# ============================================================================

EXTENSION_GUIDE = """
=============================================================================
HOW TO ADD A NEW VIEW TYPE (e.g., Mobile App)
=============================================================================

Step 1: Create new view file in views/ directory
   views/mobile_view.py

Step 2: Import formatters
   from views.formatters import BookFormatter, UserFormatter

Step 3: Create view classes for each entity
   class MobileBookView:
       @staticmethod
       def get_data(books):
           return BookFormatter.format_books(books)

Step 4: Use in your application
   from views.mobile_view import MobileBookView
   
   mobile_view = MobileBookView()
   data = mobile_view.get_data(books)


=============================================================================
HOW TO ADD A NEW MANAGER (e.g., ReservationManager)
=============================================================================

Step 1: Create model class
   models/Reservation.py
   
   class Reservation(BaseModel):
       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.user_id = kwargs.get('user_id', '')
           self.book_id = kwargs.get('book_id', '')
           self.reservation_date = kwargs.get('reservation_date', '')

Step 2: Create manager class
   models/ReservationManager.py
   
   class ReservationManager:
       def __init__(self, storage):
           self.storage = storage
       
       def reserve_book(self, user_id, book_id):
           # Business logic here
           pass

Step 3: Create formatter (optional)
   Add ReservationFormatter to views/formatters.py

Step 4: Create views (optional)
   Add ReservationView to views/cli_view.py, web_view.py, gui_view.py

Step 5: Integrate into APP.py
   from models.ReservationManager import ReservationManager
   from views.cli_view import ReservationView
   
   self.reservation_manager = ReservationManager(storage)
   self.reservation_view = ReservationView()


=============================================================================
HOW TO ADD A NEW FORMATTER
=============================================================================

Step 1: Create formatter in views/formatters.py

   class ReservationFormatter:
       @staticmethod
       def format_reservations(reservations):
           formatted = []
           for key, res in reservations.items():
               formatted.append({
                   "id": res.id,
                   "user_id": res.user_id,
                   "book_id": res.book_id,
                   "date": res.reservation_date
               })
           return formatted

Step 2: Use in views
   from views.formatters import ReservationFormatter
   
   formatted_data = ReservationFormatter.format_reservations(data)


=============================================================================
HOW TO TEST A SPECIFIC LAYER
=============================================================================

# Test Model Layer
from models.Book import Book

book = Book(title="Test", author="Author", isbn="123", 
            published_date="2023-01-01", available_copies=5, total_copies=5)
assert book.title == "Test"

# Test Manager Layer
from models.BookManager import BookManager
from models.engine.file_storage import FileStorage

storage = FileStorage()
manager = BookManager(storage)
book = manager.add_book("Test", "Author", "123", "2023-01-01", 5)
assert book is not None

# Test Formatter Layer
from views.formatters import BookFormatter

formatted = BookFormatter.format_book(book)
assert "title" in formatted

# Test View Layer
from views.cli_view import BookView

view = BookView()
# Visual inspection or capture output
view.display_book(book)
"""

# ============================================================================
# DEPENDENCIES DIAGRAM
# ============================================================================

DEPENDENCIES = """
┌──────────────────────────────────────────────────────────────────┐
│                      APP.py (Controller)                         │
│            (LibraryApp - orchestrates everything)                │
└──────────────────────────────────────────────────────────────────┘
           ↓                    ↓                    ↓
    ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐
    │ BookManager  │   │ UserManager  │   │TransactionManager    │
    │(business)    │   │(business)    │   │(business)            │
    └──────────────┘   └──────────────┘   └──────────────────────┘
           ↓                    ↓                    ↓
    ┌──────────────────────────────────────────────────────────────┐
    │              FileStorage (Persistence)                       │
    │                   (JSON serialization)                       │
    └──────────────────────────────────────────────────────────────┘
           ↑                    ↑
    ┌──────────────────────────────────────────────────────────────┐
    │ Book | User | Transaction | BaseModel (Data Models)          │
    └──────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────┐
│                      Views (Presentation)                        │
├──────────────────────────────────────────────────────────────────┤
│  CLI Views      │  Web Views      │  GUI Views      │  Mobile    │
│  (cli_view.py)  │  (web_view.py)  │  (gui_view.py)  │  Views     │
└──────────────────────────────────────────────────────────────────┘
           ↓                    ↓                    ↓
    ┌──────────────────────────────────────────────────────────────┐
    │         Formatters (formatters.py)                           │
    │   - BookFormatter      - UserFormatter                       │
    │   - TransactionFormatter   - Others                          │
    └──────────────────────────────────────────────────────────────┘
           ↑                    ↑                    ↑
    ┌──────────────────────────────────────────────────────────────┐
    │              Managers (Business Logic)                       │
    │   - BookManager  - UserManager  - TransactionManager         │
    └──────────────────────────────────────────────────────────────┘
