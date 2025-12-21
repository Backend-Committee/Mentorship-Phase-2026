import json
from datetime import date, timedelta
# ------------- Helper Functions -------------
def get_today_date():
    return date.today()

def generate_id(data):
    if not data:
        return 1
    # If a top-level dict was loaded from JSON, try to extract the list inside
    if isinstance(data, dict):
        for key in ("Books", "Visitors", "Borrowed_books", "BorrowedBooks", "BBooks"):
            if key in data and isinstance(data[key], list):
                data = data[key]
                break
        else:
            for v in data.values():
                if isinstance(v, list):
                    data = v
                    break

    # Compute max id from items, supporting keys "ID" or "id" and integer list items
    max_id = 0
    for item in data:
        if isinstance(item, dict):
            id_val = item.get("ID") if item.get("ID") is not None else item.get("id")
            if isinstance(id_val, int) and id_val > max_id:
                max_id = id_val
        elif isinstance(item, int):
            if item > max_id:
                max_id = item
    return max_id + 1

def correct_input(num_options):
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= num_options:
                return choice
            else:
                print(f"Please enter a number between 1 and {num_options}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def addBook(manager):
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    place = input("Enter book place: ")
    book_id = generate_id(manager.Books)
    new_book = Book(title, author, book_id, place)
    manager.add_book(new_book)

# ------------- Main System Function -------------
def run_system():
    manager = Manager()
    while True:
        print("\n============================================================")
        print("================= Library Management System ================")
        print("============================================================")

        print("\n\n------------- Main Menu -------------")
        print("1. Manage Books")
        print("2. Manage Visitors")
        print("3. Manage Borrowed Books")
        print("4. Exit")
        choice = correct_input(4)

# ------------- Manage Books -------------
        if choice == 1:
            while True:
                print("\n\n\n------------- Manage Books -------------")
                print("1. Add Book")
                print("2. Remove Book")
                print("3. Search Book by ID")
                print("4. Display Available Books")
                print("5. Back to Main Menu")
                book_choice = correct_input(5)
                if book_choice == 1:
                    addBook(manager)
                elif book_choice == 2:
                    try:
                        book_id = int(input("Enter Book ID to remove: "))
                        manager.remove_book(book_id)
                    except ValueError:
                        print("Invalid Book ID.")
                elif book_choice == 3:
                    try:
                        book_id = int(input("Enter Book ID to search: "))
                        manager.search_book_byID(book_id)
                    except ValueError:
                        print("Invalid Book ID.")
                elif book_choice == 4:
                    manager.display_available_books()
                elif book_choice == 5:
                    break

# ------------- Manage Visitors -------------
        elif choice == 2:
            while True:
                print("\n\n\n------------- Manage Visitors -------------")
                print("1. Add Visitor")
                print("2. Remove Visitor")
                print("3. Search Visitor by ID")
                print("4. Display All Visitors")
                print("5. Pay Fine")
                print("6. Back to Main Menu")
                visitor_choice = correct_input(6)
                if visitor_choice == 1:
                    name = input("Enter visitor name: ")
                    visitor_id = generate_id(manager.Visitors)
                    new_visitor = Visitor(name, visitor_id)
                    manager.add_visitor(new_visitor)
                elif visitor_choice == 2:
                    try:
                        visitor_id = int(input("Enter Visitor ID to remove: "))
                        manager.remove_visitor(visitor_id)
                    except ValueError:
                        print("Invalid Visitor ID.")
                elif visitor_choice == 3:
                    try:
                        visitor_id = int(input("Enter Visitor ID to search: "))
                        manager.search_visitor_byID(visitor_id)
                    except ValueError:
                        print("Invalid Visitor ID.")
                elif visitor_choice == 4:
                    manager.display_all_visitors()
                elif visitor_choice == 5:
                    try:
                        visitor_id = int(input("Enter your Visitor ID: "))
                        amount = float(input("Enter amount to pay: "))
                        manager.pay_fine(visitor_id, amount)
                    except ValueError:
                        print("Invalid input.")
                elif visitor_choice == 6:
                    break

# ------------- Manage Borrowed Books -------------
        elif choice == 3:
            while True:
                print("\n\n\n------------- Manage Borrowed Books -------------")
                print("1. Borrow Book")
                print("2. Return Book")
                print("3. Search Borrowed Book by ID")
                print("4. Display All Borrowed Books")
                print("5. Back to Main Menu")
                bbook_choice = correct_input(5)
                if bbook_choice == 1:
                    try:
                        visitor_id = int(input("Enter your Visitor ID: "))
                        book_id = int(input("Enter Book ID to borrow: "))
                        borrow_date = get_today_date()
                        days_to_return = int(input("Enter number of days to return the book: "))
                        manager.borrow_book(visitor_id, book_id, borrow_date, days_to_return)
                    except ValueError:
                        print("Invalid input.")
                elif bbook_choice == 2:
                    try:
                        visitor_id = int(input("Enter your Visitor ID: "))
                        book_id = int(input("Enter Book ID to return: "))
                        manager.return_book(visitor_id, book_id)
                    except ValueError:
                        print("Invalid input.")
                elif bbook_choice == 3:
                    try:
                        book_id = int(input("Enter Book ID to search: "))
                        manager.search_borrowed_book(book_id)
                    except ValueError:
                        print("Invalid Book ID.")
                elif bbook_choice == 4:
                    manager.display_borrowed_books()
                elif bbook_choice == 5:
                    break

# ------------- Exit System -------------        
        elif choice == 4:
            print("Exiting the system. Goodbye!")
            break

# ------------- Classes -------------
# Visitor and Book Classes with JSON representation methods only
# I handle data storage and operations in Manager class
class Visitor:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.balance = 0
        self.bbooks = []
    
    def form_json(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Balance": self.balance,
            "Borrowed_books": self.bbooks
        }
     
class Book:
    def __init__(self, title, author, id, place, available=True):
        self.title = title
        self.author = author
        self.id = id
        self.place = place
        self.available = available
    
    def form_json(self):
        return {
            "ID": self.id,
            "Title": self.title,
            "Author": self.author,
            "Place": self.place,
            "Available": self.available
        }

# ------------- Manager Class -------------
# Handles all operations and data storage
# Files: Visitors.JSON, Books.JSON, BorrowedBooks.JSON
# Methods: add/remove/search visitors/books, borrow/return books, pay fines  
class Manager:
    def __init__(self, VDB="JSONFiles\Visitors.JSON", BDB="JSONFiles\Books.JSON", BBDB="JSONFiles\BorrowedBooks.JSON"):
        self.VDB = VDB
        self.BDB = BDB
        self.BBDB = BBDB
        self.Visitors = []
        self.Books = []
        self.BBooks = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.VDB, "r") as file:
                data = json.load(file)
                if isinstance(data, dict) and "Visitors" in data and isinstance(data["Visitors"], list):
                    self.Visitors = data["Visitors"]
                elif isinstance(data, list):
                    self.Visitors = data
                else:
                    self.Visitors = []
        except FileNotFoundError:
            print("Visitor database not found. Creating a new one....")
            self.save_visitor_data()

        try:
            with open(self.BDB, "r") as file:
                data = json.load(file)
                if isinstance(data, dict) and "Books" in data and isinstance(data["Books"], list):
                    self.Books = data["Books"]
                elif isinstance(data, list):
                    self.Books = data
                else:
                    # try to find first list value inside dict
                    self.Books = []
                    if isinstance(data, dict):
                        for v in data.values():
                            if isinstance(v, list):
                                self.Books = v
                                break
        except FileNotFoundError:
            self.Books = []

        try:
            with open(self.BBDB, "r") as file:
                data = json.load(file)
                if isinstance(data, dict) and "BorrowedBooks" in data and isinstance(data["BorrowedBooks"], list):
                    self.BBooks = data["BorrowedBooks"]
                elif isinstance(data, dict) and "BBooks" in data and isinstance(data["BBooks"], list):
                    self.BBooks = data["BBooks"]
                elif isinstance(data, list):
                    self.BBooks = data
                else:
                    self.BBooks = []
        except FileNotFoundError:
            self.BBooks = []
    
    def save_visitor_data(self):
        with open(self.VDB, "w") as file:
            json.dump(self.Visitors, file, indent=4)

    def save_book_data(self):
        with open(self.BDB, "w") as file:
            json.dump(self.Books, file, indent=4)
    
    def save_bbook_data(self):
        with open(self.BBDB, "w") as file:
            json.dump(self.BBooks, file, indent=4)

    def add_book(self, book: Book):
        self.Books.append(book.form_json())
        self.save_book_data()
        print("\nBook added successfully.\nBook ID is:", book.id)

    def search_book_byID(self, book_id):
        print("\nSearching for book ID:", book_id)
        for book in self.Books:
            if book["ID"] == book_id:
                print("Book ID:", book["ID"], "\nTitle:", book["Title"], "\nAuthor:", book["Author"], "\nPlace:", book["Place"], "\nAvailable:", book["Available"])
                return
        print("\nBook not exists!!")

    def display_available_books(self):
        print("\nAvailable Books:")
        for book in self.Books:
            if book["Available"]:
                print("\nBook ID:", book["ID"], "\nTitle:", book["Title"], "\nAuthor:", book["Author"])

    def remove_book(self, book_id):
        for book in self.Books:
            if book["ID"] == book_id:
                self.Books.remove(book)
                self.save_book_data()
                print("\nBook with ID", book_id, "removed successfully.")
                return
        print("\nBook not exists!!")

    def add_visitor(self, visitor: Visitor):
        self.Visitors.append(visitor.form_json())
        self.save_visitor_data()
        print("\nVisitor added successfully.\nVisitor ID is:", visitor.id)

    def remove_visitor(self, visitor_id):
        for visitor in self.Visitors:
            if visitor["ID"] == visitor_id:
                self.Visitors.remove(visitor)
                self.save_visitor_data()
                print("\nVisitor with ID", visitor_id, "removed successfully.")
                return
        print("\nVisitor not exists!!")

    def search_visitor_byID(self, visitor_id):
        print("\nSearching for visitor ID:", visitor_id)
        for visitor in self.Visitors:
            if visitor["ID"] == visitor_id:
                print("Visitor ID:", visitor["ID"], "\nName:", visitor["Name"], "\nBalance:", visitor["Balance"], "\nBorrowed Books:", visitor["Borrowed_books"])
                return
        print("\nVisitor not exists!!")

    def display_all_visitors(self):
        print("\nAll Visitors:")
        for visitor in self.Visitors:
            print("\nVisitor ID:", visitor["ID"], "\nName:", visitor["Name"], "\nBalance:", visitor["Balance"])

    def pay_fine(self, visitor_id, amount):
        for visitor in self.Visitors:
            if visitor["ID"] == visitor_id:
                if amount == visitor["Balance"]:
                    visitor["Balance"] = 0
                    self.save_visitor_data()
                    print("\nFine paid successfully.")
                    return
                elif amount < visitor["Balance"]:
                    print("\nAmount is less than the fine balance.")
                    print("Current Balance:", visitor["Balance"])
                    return
                else:
                    print("\nAmount exceeds the fine balance.")
                    print("Current Balance:", visitor["Balance"])
                    visitor["Balance"] = 0
                    self.save_visitor_data()
                    print("\nFine paid successfully.")
                    print("Excess amount will be refunded.")
                    return
    
    def borrow_book(self, visitor_id, book_id, borrow_date, days_to_return):
        for visitor in self.Visitors:
            if visitor["ID"] == visitor_id:
                if len(visitor["Borrowed_books"]) == 5:
                    print("\nVisitor has reached the maximum limit of borrowed books.")
                    return
                if visitor["Balance"] > 0:
                    print("\nVisitor has outstanding fines. Cannot borrow books.")
                    return
                for book in self.Books:
                    if book["ID"] == book_id:
                        if book["Available"]:
                            book["Available"] = False
                            visitor["Borrowed_books"].append(book_id)
                            self.BBooks.append({
                                "Visitor_ID": visitor_id,
                                "Book_ID": book_id,
                                "Borrow_Date": borrow_date.isoformat(),
                                "Return_Date": (borrow_date + timedelta(days=days_to_return)).isoformat()
                            })
                            self.save_book_data()
                            self.save_visitor_data()
                            self.save_bbook_data()
                            print("\nBook with ID", book_id, "borrowed successfully.")
                            return
                        else:
                            print("\nBook is not available.")
                            return
                print("\nBook not exists!!")
                return
        print("\nVisitor not exists!!")

    def return_book(self, visitor_id, book_id):
        for bbook in self.BBooks:
            if bbook["Visitor_ID"] == visitor_id and bbook["Book_ID"] == book_id:
                self.BBooks.remove(bbook)
                for book in self.Books:
                    if book["ID"] == book_id:
                        book["Available"] = True
                        break
                for visitor in self.Visitors:
                    if visitor["ID"] == visitor_id:
                        returned = date.fromisoformat(bbook["Return_Date"])
                        if get_today_date() > returned:
                            days_late = (get_today_date() - returned).days
                            fine = days_late * 5  # Assuming fine is 1 unit per day
                            visitor["Balance"] += fine
                            print(f"\nBook returned late. Fine imposed: {fine} units.")
                        visitor["Borrowed_books"].remove(book_id)
                        break
                self.save_book_data()
                self.save_visitor_data()
                self.save_bbook_data()
                print("\nBook with ID", book_id, "returned successfully.")
                return
        print("\nNo record of this borrowed book found.")

    def search_borrowed_book(self, book_id):
        print("\nSearching for borrowed book ID:", book_id)
        for bbook in self.BBooks:
            if bbook["Book_ID"] == book_id:
                print("Visitor ID:", bbook["Visitor_ID"], "Return Date:", bbook["Return_Date"])
                return
        print("No record of this borrowed book found.")
    
    def display_borrowed_books(self):
        print("Borrowed Books:")
        for bbook in self.BBooks:
            print("Visitor ID:", bbook["Visitor_ID"], "Book ID:", bbook["Book_ID"], "Return Date:", bbook["Return_Date"])

# ------------- End of Manager Class -------------
# ------------- Run the System -------------
run_system()