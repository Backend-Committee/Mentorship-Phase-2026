import json

# the way to add inline json file
# booksData = '''
#         {
#             "Lord of the flies": "Borrowed",
#             "The picture of Dorian Gray": "Available"
#         }
# '''


class ManagementSystem:
    
    def __init__(self):
    # should be instance variables
        # self.__Books = {
        #     "Lord of the flies": "Borrowed",
        #     "Lord of the Rings": "Available"};
        
        # would have been used with inline json data
        # self.__Books = json.loads(booksData)
        
        with open("Tasks/Task1-LibraryManagementSystem/books.json", "r") as file:
            self.__Books = json.load(file)
        
        # you can't make a set as a json
        # self.__Users = {"Rawan Ahmed", "Mesh Rawan Ahmed"};
        with open("Tasks/Task1-LibraryManagementSystem/users.json", "r") as fi:
            self.__Users = set(json.load(fi))
       
       
    def SaveBooks(self):
        with open("Tasks/Task1-LibraryManagementSystem/books.json", "w") as file: # write
            json.dump(self.__Books, file, indent=4) #indentation
            # edits the json file
            
    def SaveUsers(self):
        with open("Tasks/Task1-LibraryManagementSystem/users.json", "w") as file:
            # json.dump(list(self.__Users), file, indent=4)
            json.dump(sorted(self.__Users), file, indent=4) # sorted list
             
    def AddBook(self, bookName):
        # a very easy way to find values in a list
        if bookName in self.__Books:
            print("Book already exists in the library!")
        else:      
            self.__Books[bookName]= "Available"
            self.SaveBooks()
            print("Book Added Successfully!")
            
    def AddUser(self, name):
        self.__Users.add(name)
        self.SaveUsers()
        print("User Added Successfully!")
    
    def BorrowBook(self, bookname):
        # for book, status in self.__Books.items():
        if bookname in self.__Books:
            if self.__Books[bookname] == "Borrowed":
                print("Sorry, the book is already borrowed")
            else:
                print("Book Borrowed successfully!")
                self.__Books[bookname] = "Borrowed"
                self.SaveBooks()
        else:
            print("Sorry, We don't have this book")
            
    def ReturnBook(self, bookname):
        if bookname in self.__Books:
           if self.__Books[bookname] == "Borrowed":
                self.__Books[bookname] ="Available"
                self.SaveBooks()
                print("Book returned successfully!")
           else: 
                print("The book is not borrowed!")
        else:
            print("Sorry, this book doesn't belong to our library")
                        
    def DisplayBooks(self):
        print("\n--- Library Books ---\n")
        # print(self.__Books);
        # for book in self.__Books:
            # print(f"{book[name]}: {book[status]}")
        for book, status in self.__Books.items():
            # we can use f before the string to insert variables in the string with {}
            # print(f"{book}: {status}")
            print(book,": ", status, "\n")
        print("-------------------\n")
        
    def DisplayUsers(self):
        print("\n--- Library Members ---\n")
        # print(self.__Books);
        # for book in self.__Books:
            # print(f"{book[name]}: {book[status]}")
        for human in self.__Users:
            # we can use f before the string to insert variables in the string with {}
            # print(f"{book}: {status}")
            print(human, "\n")
        print("-------------------\n")
    
        

library = ManagementSystem()
library.DisplayBooks()
library.AddBook("And then there were none")
library.AddUser("Ziad Ahmed")
library.DisplayBooks()

library.BorrowBook("80 Days around the world")

library.ReturnBook("Lord of the flies")
library.DisplayBooks()
library.DisplayUsers()