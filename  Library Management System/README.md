# Library Management System

A comprehensive Python-based Library Management System that allows users to manage books, users, and borrowing/returning transactions with persistent JSON-based storage.

## Author
- **Name:** Mahmoud Ahmed Ibrahim Adam
- **Email:** mahmoudadam5555@gmail.com
- **GitHub:** mahmoud-5555
- **LinkedIn:** https://www.linkedin.com/in/mahmoud-adam-bb3056248/

## Features 

### Implemented Features
- **Add Books** - Add new books with title, author, ISBN, publication date, and copy count
- **Add Users** - Register new library members
- **Borrow Books** - Allow users to borrow available books
- **Return Books** - Process book returns and update availability
- **Display Available Books** - View books currently available for borrowing
- **Display All Books** - View complete library catalog
- **Display All Users** - View all registered members
- **Display Borrowed Books** - Check what books a user has borrowed
- **Search Books** - Search for books by title
- **Transaction History** - View complete borrowing/returning history
- **JSON File Storage** - All data persists in JSON files
- **User Deactivation** - Deactivate/Activate user accounts
- **Error Handling** - Comprehensive validation and error messages

## Project Structure

```
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
│   ├── TransactionManager.py        # Transaction operations manager
│   └── engine/
│       ├── __init__.py
│       └── file_storage.py          # JSON persistence engine
│
├── views/                           # Presentation layer (multiple UI options)
│   ├── __init__.py
│   ├── formatters.py                # Data formatters (BookFormatter, UserFormatter, etc.)
│   ├── cli_view.py                  # CLI/Terminal views (BookView, UserView, TransactionView)
│   ├── web_view.py                  # Web/API views (JSON format)
│   └── gui_view.py                  # GUI/Desktop views (Tkinter, PyQt compatible)
│
├── storage/                         # Data persistence
│   ├── books.json                   # Books data
│   ├── users.json                   # Users data
│   └── transactions.json            # Transactions data
│
├── APP.py                           # Main CLI application
├── test_refactored.py               # Refactoring verification tests
├── ARCHITECTURE.md                  # Detailed architecture documentation
└── README.md                        # This file
```

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup
1. Navigate to the project directory:
```bash
cd "Library Management System"
```

## Usage

### Running the Application

Start the interactive menu:
```bash
python3 APP.py
```

### Main Menu Options

```
1.  Add Book                    - Add a new book to the library
2.  Add User                    - Register a new library member
3.  Borrow Book                 - Borrow a book (requires User ID & Book ID)
4.  Return Book                 - Return a borrowed book
5.  Display Available Books     - View all books with available copies
6.  Display All Books           - View complete library catalog
7.  Display All Users           - View all registered members
8.  Display My Borrowed Books   - View your currently borrowed books
9.  Display All Transactions    - View complete transaction history
10. Search Book by Title        - Search for a book by its title
11. User Borrowed History       - View a user's borrowing history
0.  Exit                        - Exit the application
```

## Testing
no Unit test yet 
## Architecture Overview

This system uses **layered architecture** with separation of concerns for maximum scalability:

### Architecture Layers

```
┌─────────────────────────────────────┐
│   Presentation Layer (Views)        │
│  CLI | Web API | GUI | Mobile       │
└─────────────────────────────────────┘
              ↓ Uses
┌─────────────────────────────────────┐
│   Formatting Layer (Formatters)     │
│   BookFormatter | UserFormatter     │
└─────────────────────────────────────┘
              ↓ Uses
┌─────────────────────────────────────┐
│   Business Logic (Managers)         │
│  BookManager | UserManager | etc.   │
└─────────────────────────────────────┘
              ↓ Uses
┌─────────────────────────────────────┐
│   Data Layer (Models)               │
│  Book | User | Transaction          │
└─────────────────────────────────────┘
```

### Key Benefits

- **Separation of Concerns**: Each layer has a single responsibility
- **Reusability**: Same managers work with CLI, Web, GUI, Mobile
- **Scalability**: Add new view types without modifying existing code
- **Testability**: Test each layer independently
- **Maintainability**: Clear dependencies and organization

### View Implementations

- **CLI Views** (`cli_view.py`): Console/terminal formatted output
- **Web Views** (`web_view.py`): JSON responses for REST APIs
- **GUI Views** (`gui_view.py`): Data structures for Tkinter/PyQt applications
- **Extensible**: Add mobile views, desktop apps, or other UIs easily

## Data Storage

All data is automatically saved to JSON files in the `storage/` directory. Each entity type (Book, User, Transaction) has its own JSON file with complete serialization of all object data.

## Usage Examples

### Using CLI View (Current Implementation)
```python
from models.BookManager import BookManager
from views.cli_view import BookView

book_manager = BookManager(storage)
book_view = BookView()

# Add and display books
book = book_manager.add_book("Python 101", "John Doe", "123-456", "2023-01-01", 5)
all_books = book_manager.get_all_books()
book_view.display_books(all_books)  # Pretty printed table
```

### Using Web View (REST API)
```python
from models.BookManager import BookManager
from views.web_view import WebBookView

book_manager = BookManager(storage)
web_view = WebBookView()

# Get books as JSON
all_books = book_manager.get_all_books()
json_response = web_view.get_books_json(all_books)
# Output: {"status": "success", "data": [...], "count": 1}
```

### Using GUI View (Tkinter/PyQt)
```python
from models.BookManager import BookManager
from views.gui_view import GUIBookView

book_manager = BookManager(storage)
gui_view = GUIBookView()

# Get books for table display
all_books = book_manager.get_all_books()
table_rows = gui_view.get_books_for_table(all_books)
# Returns: [(id, title, author, isbn, available, total), ...]
```

### Adding a Custom View
```python
# Create views/mobile_view.py
from views.formatters import BookFormatter

class MobileBookView:
    @staticmethod
    def get_compact_books(books):
        formatted = BookFormatter.format_books(books)
        return [{"id": b["id"], "title": b["title"], "available": b["available_copies"]} 
                for b in formatted]
```

## Error Handling

The system includes comprehensive error handling:
- User validation before transactions
- Book availability checking
- Account status verification
- Transaction history tracking
- Graceful error messages

## Class Architecture

### Models Layer
- **BaseModel**: Base class providing UUID, timestamps, and serialization
- **Book**: Book entity with availability tracking
- **User**: User entity with membership status
- **Transaction**: Transaction record for borrow/return operations

### Managers Layer (Business Logic)
- **BookManager**: Book CRUD operations and queries
- **UserManager**: User CRUD operations and account management
- **TransactionManager**: Borrow/return logic with validation

### Views Layer (Presentation)
- **BookView/UserView/TransactionView**: CLI formatted output
- **WebBookView/WebUserView/WebTransactionView**: JSON API responses
- **GUIBookView/GUIUserView/GUITransactionView**: GUI table/form data structures

### Support Layer
- **BookFormatter/UserFormatter/TransactionFormatter**: Data transformation
- **FileStorage**: JSON persistence engine

## Extending the System

### Adding a New View Type
1. Create a new file in `views/` directory (e.g., `mobile_view.py`)
2. Import formatters and create view classes
3. Implement methods to format data for your UI
4. Use in your application alongside existing views

### Adding a New Manager
1. Create model in `models/` directory
2. Create manager class with business logic
3. Add formatter for the data
4. Create view classes in each UI layer
5. Integrate into `APP.py`

### Adding a Database Backend
1. Replace `FileStorage` with database adapter
2. Implement same interface as `FileStorage`
3. Managers and views remain unchanged!

## Future Enhancements

- Due date tracking and late fees
- Book reservations
- Email notifications
- Advanced analytics and reporting
- Mobile app (using mobile_view.py)
- Web dashboard (using Flask/Django with web_view.py)
- Desktop GUI (using Tkinter/PyQt with gui_view.py)

## License

This project is for educational purposes.

## Documentation

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md)
