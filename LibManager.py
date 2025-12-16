import json

class Books:
    def __init__(self, name, BID, author, flag=True):
        self.name = name
        self.BID = BID
        self.author = author
        self.flag = flag

    def JSONForm(self):
        return{
            "BID": self.BID,
            "BName": self.name,
            "author": self.author,
            "flag": self.flag
        }
    
class User:
    def __init__(self, name, UID):
        self.name = name
        self.UID = UID
        self.LoBB = []

    def JSONForm(self):
        return{
            "UID": self.UID
            ,"UName": self.name
            ,"BorrowedBooks": self.LoBB
        } 

class Library:
    def __init__(self, DB="library.json"):
        self.DB = DB
        self.Books = []
        self.Users = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.DB, "r") as f:
                data = json.load(f)
                self.Books = data["Books"]
                self.Users = data["Users"]
        except FileNotFoundError:
            self.save_data()
    
    def save_data(self):
        with open(self.DB, "w") as f:
            json.dump(
                {"Books": self.Books, "Users": self.Users}, f , indent=4
            )
    
    def addBook(self, book: Books):
        self.Books.append(book.JSONForm())
        self.save_data()
    
    def addUser(self, user: User):
        self.Users.append(user.JSONForm())
        self.save_data()
    
    def displayAvailableBooks(self):
        for book in self.Books:
            if book["flag"]:
                print(book["BID"], book["BName"])

    def borrowBook(self, UID, BID):
        for book in self.Books:
            if book["BID"] == BID and book["flag"]:
                book["flag"] = False
        
            for user in self.Users:
                if user["UID"] == UID:
                    user["BorrowedBooks"].append(BID)
                    self.save_data()
                    print(f"Book borrowed successfully")
                    return
        print(f"Book not available")

    def returnBook(self, UID, BID):
        for user in self.Users:
            if user["UID"] == UID and BID in user["BorrowedBooks"]:
                user["BorrowedBooks"].remove(BID)

                for book in self.Books:
                    if book["BID"] == BID:
                        book["flag"] = True
                        self.save_data()
                        print(f"Book returned successfully")
                        return
        print("Return failed!")

lib = Library()

lib.addBook(Books("The Alchemist", 1, "Paulo Coelho"))
lib.addBook(Books("Eleven Minutes", 2, "Paulo Coelho"))
lib.addUser(User("Yousef Hosni", 20231210))

lib.borrowBook(20231210, 1)
lib.displayAvailableBooks()
lib.returnBook(20231210, 1)
lib.displayAvailableBooks()