import pickle
import os

class Book:

    num_of_books = 0
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.available = True
        Book.num_of_books += 1
    def __str__(self):
        return f"Tile: {self.title} || Author: {self.author} || Available: {self.available}"

########################################################################################################################
class User:

    num_of_users = 0
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
        User.num_of_users += 1

    # @classmethod
    # def print_users_number(cls):
    #     print(f"The number of users is : {cls.num_of_users}\n")
    #
    # def all_user_info(self):
    #     return f"Name: {self.name}\nEmail: {self.email}\nAge: {self.age}"

########################################################################################################################
class Customer(User):

    num_of_customers = 0
    def __init__(self, name, email, age, ID):
        super().__init__(name, email, age)
        self.ID = ID
        Customer.num_of_customers += 1

    def __str__(self):
        return f"Name : {self.name} || Email : {self.email} || Age : {self.age} || ID : {self.ID}"

########################################################################################################################
class Worker(User):

    num_of_workers = 0
    def __init__(self, name, email, age, salary, workerID):
        super().__init__(name, email, age)
        self.salary = salary
        self.workerID = workerID
        Worker.num_of_workers += 1

    def __str__(self):
        return f"Name : {self.name} || Email : {self.email} || Salary : {self.salary} || WorkerID : {self.workerID}"

########################################################################################################################
class library:

    def __init__(self):
        print("Welcome to the library !".upper())
        self.books = []
        self.customers = []
        self.workers = [Worker("Bassam", "bassam@gmail.com", 19, 1000000, 666)]
        self.borrowed_books = {}

    def save_data(self):
        with open("library_data.pkl", "wb") as file:  # wb = write binary
            pickle.dump(self, file)

    def add_book(self, title, author):
        self.books.append(Book(title, author))
        self.save_data()
        print("The book has been added to the library")

    def remove_book(self, title, author):
        for book in self.books:
            if book.title == title and book.author == author:
                self.books.remove(book)
                self.save_data()
        print("The book has been removed from the library")

    def add_customer(self, name, email, age, ID):
        self.customers.append(Customer(name, email, age, ID))
        self.save_data()
        print("The customer has been added to the system")

    def add_worker(self, name, email, age, salary, workerID):
        self.workers.append(Worker(name, email, age, salary, workerID))
        self.save_data()
        print("The worker has been added to the system")

    def is_worker(self, ID):
        for worker in self.workers:
            if worker.workerID == ID:
                print(f"\nWelcome Mr/Ms {worker.name}")
                return worker
        return False

    def is_customer(self, ID):
        for customer in self.customers:
            if customer.ID == ID:
                print(f"\nWelcome Mr/Ms {customer.name}")
                return customer
        return False

    def show_books(self):
        print(f"\nThere are {len(self.books)} books available")
        i = 1
        for book in self.books:
            print(f"{i}- {book}")
            i += 1

    def show_customer_list(self):
        print()
        i = 1
        for customer in self.customers:
            print(f"{i}- {customer}")
            i += 1

    def show_workers_list(self):
        print()
        i = 1
        for worker in self.workers:
            print(f"{i}- {worker}")
            i += 1

    def borrow_book(self, customer_obj, title_of_book, author):
        for book in self.books:
            if book.title == title_of_book and book.author == author:
                if book.available:
                    book.available = False
                    self.borrowed_books.update({book : customer_obj})
                    self.save_data()
                    print(f"The book has been borrowed successfully by {customer_obj.name}")
                else:
                    print(f"{book}\n is not available right now")
                break
        else:
            print("There is no book with that name and author")

    def return_borrowed_book(self, name_of_customer, title_of_book, author):
        for book in self.books:
            if book.title == title_of_book and book.author == author:
                if book.available:
                    print(f"{book}\n is available not borrowed right now")
                else:
                    book.available = True
                    print(f"The book is successfully returned by {name_of_customer}")
                    self.borrowed_books.pop(book)
                    self.save_data()

    def show_borrowed_books(self):
        if len(self.borrowed_books) == 0:
            return "There is no borrowed books"
        else:
            for key, value in self.borrowed_books.items():
                print(f"Book : {key.title}\n"
                      f"author: {key.author}\n"
                      f"borrowed by {value}")

###########################################   Main program   ################################################################

def load_library():
    try:
        with open("library_data.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return library()

lib = load_library()

print("1- Im a Worker ")
print("2- Im a Customer ")
f_choice = int(input("Enter your choice: "))

if f_choice == 1:
    worker = lib.is_worker(int(input("Enter your Worker ID: ")))
    if worker:
        while True:
            print("\n0- Exit")
            print("1- Add Book")
            print("2- Remove Book")
            print("3- Add Customer")
            print("4- Add Worker")
            print("5- Show Books")
            print("6- show borrowed books list")
            print("7- Show customers list")
            if worker.workerID == 666:
                print("8- Show workers list (Manager only)")
                print("9- Reset the system (Manager only)")

            choice = int(input("Please Enter your choice: "))
            if choice == 0:
                break

            elif choice == 1:
                lib.add_book(input("\nPlease enter the title of the book: "),
                             input("Please enter the authors name: "))

            elif choice == 2:
                lib.show_books()
                lib.remove_book(input("\nPlease enter the title of the book: "),
                                input("Please enter the authors name: "))

            elif choice == 3:
                lib.add_customer(input("\nPlease enter the name of the customer:"),
                                 input("Please enter the email address: "),
                                 int(input("Please enter the age: ")),
                                 int(input("Please enter the ID: ")))

            elif choice == 4:
                lib.add_worker(input("\nPlease enter the name of the worker: "),
                               input("Please enter the email address: "),
                               int(input("Please enter the age: ")),
                               int(input("Please enter the salary: ")),
                               int(input("Please enter the work ID: ")))

            elif choice == 5:
                lib.show_books()

            elif choice == 6:
                lib.show_borrowed_books()

            elif choice == 7:
                lib.show_customer_list()

            elif choice == 8:
                if worker.workerID == 666:
                    lib.show_workers_list()
                else:
                    print("\nThe manger only can see the workers information")

            elif choice == 9:
                if worker.workerID == 666:
                    if (bool(input("\nAre you sure MR Bassam ?\npress 1 if yes "))
                            and os.path.exists("library_data.pkl")):
                        os.remove("library_data.pkl")
                        print("System has been reset. Please restart the program.")
                        exit()
                else:
                    print("\nThe manger only can reset the system")

    else:
        print("\nInvalid worker ID")

elif f_choice == 2:
    customer = lib.is_customer(int(input("Please enter the customer ID: ")))
    if customer:
        while True:
            print("\n0- Exit")
            print("1- Borrow book")
            print("2- Return borrowed book")
            print("3- Show books")
            choice = int(input("Please Enter your choice: "))
            if choice == 0:
                break

            elif choice == 1:
                lib.show_books()
                lib.borrow_book(customer, input("\nPlease enter the title of the book: "),
                                input("Please enter the authors name: "))

            elif choice == 2:
                print("\n The books you are borrowed are \n")
                for key, value in lib.borrowed_books.items():
                    if value == customer:
                        print(f"{key}  -  {value}")
                lib.return_borrowed_book(customer.name, input("\nPlease enter the title of the book: "),
                                         input("Please enter the authors name: "))

            elif choice == 3:
                print()
                lib.show_books()
    else:
        print("Invalid customer ID\n",
              "Please let a worker add you")