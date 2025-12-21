import json

class User :

    def __init__(self, ID, name, borrowedBooks = None):
        self.ID = ID
        self.name = name
        self.borrowedBooks = borrowedBooks if borrowedBooks is not None else []
    def toDict(self):
        return {
            'ID': self.ID,
            'name': self.name,
            'borrowedBooks': self.borrowedBooks
        }

class Book :
    def __init__(self,bookID,title,author,available=True):
        self.bookID = bookID
        self.title = title
        self.author = author
        self.available = available
    def toDict(self):
        return {
            'bookID': self.bookID,
            'title': self.title,
            'author': self.author,
            'available': self.available
        }

class LibrarySystem :
    def __init__(self):

        self.users = []
        self.books = []
        self.borrowed_books = {}
        self.loadData()


    def loadData(self,filename = 'library_data.json'): 
        try:
            with open(filename, 'r') as file:
                if file.read().strip():
                    file.seek(0)
                    data = json.load(file)
                    self.books = [Book(**b) for b in data["books"]]
                    self.users = [User(**u) for u in data["users"]]
                else:
                    print("Data file is empty. Starting with empty library.")
        except FileNotFoundError:
            print("Data file not found. Starting with empty library.")
        except json.JSONDecodeError:
            print("Invalid JSON format in data file. Starting with empty library.")
    def saveData(self,filename = 'library_data.json'):
        with open(filename,'w') as file:
            data = {
                'books':[b.toDict() for b in self.books],
                'users':[u.toDict() for u in self.users]
            }
            json.dump(data,file,indent=4)
    def addUser(self,userID,name):
        user = next((u for u in self.users if u.ID == userID), None)
        if user:
            print("User ID already exists.")
            return
        self.userID = userID
        new_user = User(self.userID,name)
        self.users.append(new_user)
        self.saveData()
        print(f"User '{name}' added with ID {self.userID}.")
    def addBook(self,bookID,title,author):
        book = next((b for b in self.books if b.bookID == bookID), None)
        if book:
            print("Book ID already exists.")
            return
        self.bookID = bookID
        new_book = Book(self.bookID,title,author)
        self.books.append(new_book)
        self.saveData()
        print(f"Book '{title}' by {author} added with ID {self.bookID}.")
    def borrowBook(self,userID,bookID):
        user = next((u for u in self.users if u.ID == userID), None)
        book = next((b for b in self.books if b.bookID == bookID), None)
        if not user:
            print("User ID not found.")
            return
        if not book:
            print("Book ID not found.")
            return
        if not book.available :
            print("Book is currently not available.")
            return
        user.borrowedBooks.append(bookID)
        book.available = False
        self.saveData()
        print(f"Book ID {bookID} borrowed by User ID {userID}.")
    def returnBooks (self,userID,bookID):
        user = next((u for u in self.users if u.ID == userID), None)
        book = next((b for b in self.books if b.bookID == bookID), None)
        if not user:
            print("User ID not found.")
            return
        if not book:
            print("Book ID not found.")
            return
        if bookID not in user.borrowedBooks:
            print("This book was not borrowed by the user.")
            return
        user.borrowedBooks.remove(bookID)
        book.available = True
        self.saveData()
        print(f"Book ID {bookID} returned by User ID {userID}.")

    def avilableBooks(self):
        print("Available Books:")
        for book in self.books:
            if book.available:
                print(f"ID: {book.bookID}, Title: {book.title}, Author: {book.author}")
    def displayUsers(self):
        print("Registered Users:")
        for user in self.users:
            print(f"ID: {user.ID}, Name: {user.name}, Borrowed Books: {user.borrowedBooks}")


library = LibrarySystem()
while True:
    print("\nLibrary System Menu:")
    print("1. Add User")
    print("2. Add Book")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. View Available Books")
    print("6. display users")
    print("7. Exit")


    choice = input("Enter your choice: ")

    if choice == "1":
        userID = int(input("Enter user ID: "))
        name = input("Enter user name: ")
        library.addUser(userID,name)
    elif choice == "2":
        bookID = int(input("Enter book ID: "))
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        library.addBook(bookID,title, author)
    elif choice == "3":
        userID = int(input("Enter user ID: "))
        bookID = int(input("Enter book ID: "))
        library.borrowBook(userID, bookID)
    elif choice == "4":
        userID = int(input("Enter user ID: "))
        bookID = int(input("Enter book ID: "))
        library.returnBooks(userID, bookID)
    elif choice == "5":
        library.avilableBooks()
    elif choice == "6":
        library.displayUsers()
    elif choice == "7":
        print("Exiting the Library System. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")