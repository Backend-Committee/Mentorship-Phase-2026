class Book:
   def __init__(self,title,author,is_available=True):
       self.title=title
       self.author=author
       self.is_available=is_available
   def disPlay_info(self):
       return(
           f"The Book Name : {self.title}\n"
           f"The Book Author : {self.author}\n"
           f"The Book Avaliable Or Not : {self.is_available}\n"
           )

class User:
    def __init__(self, name, user_id):
        self.name = name
        self.id = user_id
        self.borrowed_books = []

    def display_info(self):
        """
        Dispaly user information
        """
        return (
            f"User Name: {self.name}\n"
            f"User ID: {self.id}\n"
            f"Borrowed Books: {[book.title for book in self.borrowed_books]}\n"
        )

class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def borrow_book(self, book, user):
        if book.is_available:
            book.is_available = False
            user.borrowed_books.append(book)
            return f"{user.name} borrowed {book.title}"
        else:
            return f"{book.title} is not available"

    def return_book(self, book, user):
        if book in user.borrowed_books:
            book.is_available = True
            user.borrowed_books.remove(book)
            return f"{user.name} returned {book.title}"
        else:
            return f"{user.name} did not borrow {book.title}"

    def display_available_books(self):
        for book in self.books:
            if book.is_available:
                print(book.disPlay_info())


lib = Library()
while True:
    print("\n--- Library Menu ---")
    print("1. Add Book")
    print("2. Add User")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Display Available Books")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        book = Book(title, author)
        lib.add_book(book)
        print("Book added successfully")

    elif choice == "2":
        name = input("Enter user name: ")
        user_id = input("Enter user ID: ")
        user = User(name, user_id)
        lib.add_user(user)
        print("User added successfully")

    elif choice == "3":
        user_name = input("Enter user name: ")
        book_title = input("Enter book title: ")

        user = next((u for u in lib.users if u.name == user_name), None)
        book = next((b for b in lib.books if b.title == book_title), None)

        if user and book:
            print(lib.borrow_book(book, user))
        else:
            print("User or Book not found")

    elif choice == "4":
        user_name = input("Enter user name: ")
        book_title = input("Enter book title: ")

        user = next((u for u in lib.users if u.name == user_name), None)
        book = next((b for b in lib.books if b.title == book_title), None)

        if user and book:
            print(lib.return_book(book, user))
        else:
            print("User or Book not found")

    elif choice == "5":
        lib.display_available_books()

    elif choice == "6":
        print("Goodbye 👋")
        break

    else:
        print("Invalid choice")
