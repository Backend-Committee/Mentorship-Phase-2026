import json

# the way to add inline json file
# booksData = '''
#         {
#             "Lord of the flies": "Borrowed",
#             "The picture of Dorian Gray": "Available"
#         }
# '''

#classes have to start capital  
class Book:       
    def __init__(self, name, year="Unknown", genre="Unknown", author="Unknown", status="Available"):
        self.name = name;
        self.year = year;
        self.genre = genre;
        self.author = author;
        self.status = status
        
    #to detect wether the book is actually available or not
    def borrow(self):
        if self.status == "Available":
            self.status = "Borrowed"
            return True
        return False
    
    
    #to detect wether the book is actually borrowed or not
    def return_book(self):
        if self.status == "Borrowed":
            self.status = "Available"
            return True
        return False
    
    def to_dict(self):
        return {
            "name": self.name,
            "year": self.year,
            "genre": self.genre,
            "author": self.author,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        # ! see about this
        return Book(
            # data["name"] ? data["name"]: "Unknown",
            data["name"],
            data["year"],
            data["genre"],
            data["author"],
            data["status"]
        )

    
class User:
    def __init__ (self, name, userID):
        self.name = name
        self.userId = userID
        self.books = []
    
    def borrow(self, bookName):
        self.books.append(bookName)
    
    # to detect wether the user has this book or not 
    def returnBook(self, bookName):
        if bookName in self.books:
            self.books.remove(bookName)
            return True
        return False
    
    def to_dict(self):
        return {
            "name": self.name,
            "userId": self.userId,
            "Books": self.books
        }

    @staticmethod
    def from_dict(data):
        u = User(data["name"], data["userId"])
        u.books = data["Books"]
        return u
        

class ManagementSystem:
    
    def __init__(self):
    # should be instance variables
        # self.__Books = {
        #     "Lord of the flies": "Borrowed",
        #     "Lord of the Rings": "Available"};
        
        # would have been used with inline json data
        # self.__Books = json.loads(booksData)
        
        # with open("Tasks/Task1-LibraryManagementSystem/books.json", "r") as file:
        #     self.__Books = json.load(file)
        
        # # you can't make a set as a json
        # # self.__Users = {"Rawan Ahmed", "Mesh Rawan Ahmed"};
        # with open("Tasks/Task1-LibraryManagementSystem/users.json", "r") as fi:
        #     self.__Users = set(json.load(fi))
       
        # self.__Books: list[Book] = []
       self.__Books = []
       self.__Users = [] # a list of a certain type
       self.loadData()
       
    def loadData(self):
        """loads the data from json
        """
        try:
            with open("books.json", "r") as file:
                data = json.load(file)
                for book in data:
                    self.__Books.append(Book.from_dict(book))

        except FileNotFoundError:
            print("No book found in the library, starting fresh!")
            
        try:
            # you can't make a set as a json
            # self.__Users = {"Rawan Ahmed", "Mesh Rawan Ahmed"};
        # with open("Tasks/Task1-LibraryManagementSystem/users.json", "r") as fi:
            with open("users.json", "r") as fi:
                data = json.load(fi)
                for user in data:
                    self.__Users.append(User.from_dict(user))
        except FileNotFoundError:
            print("No previous Users found, starting fresh!") 
                
    def SaveBooks(self):
        with open("books.json", "w") as file: # write
            json.dump([book.to_dict() for book in self.__Books], file, indent=4) #indentation
            # edits the json file
            
    def SaveUsers(self):
        # the terminal sees what is the folder you are running the file in 
        with open("users.json", "w") as file:
            # json.dump(list(self.__Users), file, indent=4)
            json.dump([user.to_dict() for user in self.__Users], file, indent=4) # sorted list
             
    def AddBook(self, bookName):
        # a very easy way to find values in a list
        
        # if any(book.name == bookName for book in self.__Books):
        #   print("Book already exists in the library!")
        #   return
        
        for book in self.__Books:
            if bookName == book.name:
                print("Book already exists in the library!")
                return
            
        year = input("Please enter the year it was published for private purposes: ")
        genre = input("Please enter the genre (better be mystery or else): ")
        if genre.casefold() != "mystery".casefold():
            print("Why not mystery *_*")
        else:
            print("Good job")
        author = input("Please enter the author of this masterpiece: ")
    
        self.__Books.append(Book(bookName, year, genre, author))
        self.SaveBooks()
        print("Book Added Successfully! ohoo!")
        
    def AddUser(self, name, id):
        if any (user.userId == id for user in self.__Users):
            print("Sorry, this id is already taken man! Try being a little unique next time -_-")
        self.__Users.append(User(name,id))
        self.SaveUsers()
        print("User Added Successfully!")
    
    def showAllBooks(self):
        print("\n" + "*" *10)
        print("\n Library Books")
        print("\n" + "*" *10)
        for book in self.__Books:
            print("\n" + book.name)
        
    def showAvailableBooks(self):
        print("\n" + "*" *20)
        print("Library Books")
        print("\n" + "*" *20)
        for book in self.__Books:
            if book.status == "Available":
                print("\n" + book.name)
    
    # false if not available
    # def BorrowBook(self, bookName):
    #     # for book, status in self.__Books.items():
    #     for book in self.__Books:
    #         if bookName == book.name:       
    #             if book.status == "Borrowed":
    #                 print("Sorry, the book is already borrowed")
    #             else:
    #                 print("Book Borrowed successfully!")
    #                 book.status = "Borrowed"
    #                 self.SaveBooks()
    #             return
        
    #     print("Sorry, We don't have this book")
    
    # false if not available
    def BorrowBook(self, bookName, id):
        # for book, status in self.__Books.items():
        user = next((u for u in self.__Users if u.userId == id), None)
        if user is None:
            print("User not found! Please register first.")
            return
        for book in self.__Books:
            if bookName == book.name:       
                if book.borrow():
                    print("Book Borrowed successfully!")
                    user.borrow(bookName)
                    self.SaveUsers()
                    self.SaveBooks()
                else:
                    print("Sorry, the book is already borrowed")
                return
        
        print("Sorry, We don't have this book")
            
    def ReturnBook(self, bookName, userId):
        for book in self.__Books:  
            if bookName == book.name:
                if book.status == "Borrowed":
                        book.status ="Available"
                        self.SaveBooks()
                        print("Book returned successfully!")
                else: 
                        print("The book is not borrowed!")
                        
                return
        
        print("Sorry, this book doesn't belong to our library")
                        
    def DisplayBooks(self):
        print("\n--- Library Books ---\n")
        
        if not self.__Books:  # Check if list is empty
            print("No books in the library yet!")
            print("-------------------\n")
            return
        
        # print(self.__Books);
        # for book in self.__Books:
            # print(f"{book[name]}: {book[status]}")
        
        # stupid
        # for book, year, genre, author, status in self.__Books.items():
            # we can use f before the string to insert variables in the string with {}
            # print(f"{book}: \n  year: {year} \n genre: {genre} \n author:{author} \n status:{status}")
            # print(book,": ", status, "\n")
            
        for book in self.__Books:
            print(f"{book.name}:")
            print(f"  Year: {book.year}")
            print(f"  Genre: {book.genre}")
            print(f"  Author: {book.author}")
            print(f"  Status: {book.status}\n")
        print("-------------------\n")
        
    def DisplayUsers(self):
        print("\n--- Library Members ---\n")
        # print(self.__Books);
        # for book in self.__Books:
            # print(f"{book[name]}: {book[status]}")
        # for human, identification in self.__Users.items():
        #     # we can use f before the string to insert variables in the string with {}
        #     print(f"{human}: {identification}")
        #     # print(human, "\n")
        
        if not self.__Users:  # Check if empty
            print("No users registered yet!")
            print("-------------------\n")
            return
    
        for user in self.__Users:  # Loop through User objects
            borrowed = ", ".join(user.books) if user.books else "None"
            print(f"{user.name} (ID: {user.userId})")
            print(f"  Books borrowed: {borrowed}\n")
        
        print("-------------------\n")
    
        

library = ManagementSystem()
# library.DisplayBooks()
# library.AddBook("And then there were none")
# library.AddUser("Ziad Ahmed")
# library.DisplayBooks()

# library.BorrowBook("80 Days around the world")

# library.ReturnBook("Lord of the flies")
# library.DisplayBooks()
# library.DisplayUsers()

def DisplayMenu():
    print("\n" + "="*40)
    print("   LIBRARY MANAGEMENT SYSTEM")
    print("="*40)
    print("1. Display All Books")
    print("2. Add New Book")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Display All Users")
    print("6. Add New User")
    print("7. Exit")
    print("="*40)

def main():
    library = ManagementSystem()
    
    while True:
        DisplayMenu()
        choice = input("\nEnter your choice (1-8): ")
        
        if choice == "1":
            library.DisplayBooks()
        
        elif choice == "2":
            name = input("Enter book name: ")
            while name == "":
                print("Enter a real book name!")
                name = input("Enter book name: ")
                
            library.AddBook(name)
        
        elif choice == "3":
            user_id = input("Enter your user ID: ")
            library.showAvailableBooks()
            book_name = input("Enter book name to borrow: ")
            library.BorrowBook(book_name, user_id)
        
        elif choice == "4":
            book_name = input("Enter book name to return: ")
            library.ReturnBook(book_name)
        
        elif choice == "5":
            library.DisplayUsers()
        
        elif choice == "6":
            name = input("Enter user name: ")
            user_id = input("Enter user ID: ")
            
            while name == "" or id == "":
                print("Really? type real data this time")
                name = input("Enter user name: ")
                user_id = input("Enter user ID: ")
            library.AddUser(name, user_id)
        
        elif choice == "7":
            print("Thank you for using the Library System!")
            break
           
        else:
            print("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")  # Pause before showing menu again

# to treat the file as a standalone if run directly, and import it as a module if needed
if __name__ == "__main__":
    main()
    
    
# ! connect the user class
# ! Add new choices
# ! menu for books
# ! use inquirer
# ! still needs to divide classes
# ! make a good task out of this 