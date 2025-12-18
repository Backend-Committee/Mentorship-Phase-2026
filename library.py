class Users():
    def __init__(self, name = "", age = 0):
        self.name = name
        self.age = age
        self.borrowed_books = []

    def welcome(self):
        print(f"Welcome!! {self.name}")    


    def borrow_book(self, book):
        if book.available:
            book.available = False
            self.borrowed_books.append(book)
            print(f"{self.name} borrowed {book.title}")
        else:
            print("Book isn't Available at the moment..")

    def return_book(self, book):
        if book in self.borrowed_books:
            book.availabe = True
            self.borrowed_books.remove(book)
            print(f"{self.title} returned successfully! returned by: {self.name}")
        else:
            print(f"{self.name} doesn't have the book {self.title}")

users_list = []

def add_user():
    name = input("Enter your Name: ")
    age = input("Enter Age:  ")
    new_user = Users(name, age)
    users_list.append(new_user)
    new_user.welcome()
    return new_user


class Books():
    def __init__(self, title = "", author = "", year = 0, available = True):
        self.title = title
        self.author = author
        self.year = year    
        self.available = available


    def properties(self):
        status = "Available" if self.available else "Not Available"
        print(f'''Book Properties: 
----------------------              
Book Name: {self.title}
Book Author: {self.author}
Release Date: {self.year}
Availability: {status}
''')

books = []
def add_book():
    title = input("Book Title: ")
    author = input("Author: ")
    year = input("Year Published: ")
    new_book = Books(title, author, year, available = True)
    books.append(new_book)
    print(f"Book {new_book.title} added successfully!")
    return new_book


user1 = add_user()
book1 = add_book()

user2 = add_user()
book2 = add_book()



print(f"\nTotal users: {len(users_list)}")
for user in users_list:
    print(f"- {user.name} ,{user.age} years old")

print(f"\n Number of Books: {len(books)}")
for book in books:
    status = "Available" if book.available else "Unavailable"
    print(f"- Book name : {book.title}, By : {book.author}, {[status]}")