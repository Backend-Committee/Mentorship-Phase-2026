'''
-- Star Union Back-end committee sprint 1 task --
-- By: Zeyad Amin --
'''
import json

class Book:
    def __init__(self , id , title, author_name, publisher, year_of_publish):
        self.id = id
        self.title = title
        self.author_name = author_name 
        self.publisher = publisher
        self.year_of_publish = year_of_publish
        self.borrowed = False
        self.borrowed_by = None


class User:
    def __init__(self ,id ,name , phone_number):
        self.id = id
        self.name = name 
        self.phone_number = phone_number

class Library:  # The Manager (El-big boss bta3na)
    def __init__(self):
        pass

    def add_book(self,book):
        books = self.load_books()
        for bk in books:
            if bk['title'] == book.title:
                print("Book is already exists, there is a samilir title")
                return
        self.save_books(book)

    def add_customer(self,customer):
        customers = self.load_customers()
        for cust in customers:
            if cust["name"] == customer.name:
                print('Customer already exists')
                return
        self.save_customers(customer)
    
    def find_customer(self,id , customers):
        for cust in customers:
            if cust['id'] == id:
                return cust
        return -1

    def borrow_book(self, book_title, customer_name , id):
        customers = self.load_customers()
        found = self.find_customer(id , customers)
        if found == -1:
            phone_number = int(input("please enter your phone number: "))
            self.add_customer(User(id = id , phone_number= phone_number , name= customer_name))
            self.save_customers()
        books = self.load_books()
        for book in books:
            if book['title'] == book_title and not book['borrowed']:
                book['borrowed'] = True
                book['borrowed_by'] = customer_name
                print(f'book {book['title']} is successfully borrowed by: {customer_name}')
                with open("library_book.json", "w") as file:
                    json.dump(books, file, indent=4)

            elif book['title'] == book_title and book['borrowed']:
                print(f"this book is already borrowed by: {book['borrowed_by']}.")
            


    def return_book(self , book_title):
        books = self.load_books()
        for book in books:
            if book['title'] == book_title:
                book['borrowed'] = False
                book['borrowed_by'] = None
                with open("library_book.json", "w", encoding="utf-8") as file:
                    json.dump(books, file, indent=4)
                print("book had successfully returned")
                
                break

    def display_available_books(self):
        books = self.load_books()
        for book in books:
            if not book['borrowed']:
                print(f'''
ID: {book['id']}, Book Title: {book['title']}, Author Name: {book['author_name']}, 
Publisher: {book['publisher']}, Year of Publish: {book['year_of_publish']}
''')
                
    def conver_customer_to_json(self, customer):
        return {
        "id": customer.id,
        "name": customer.name,
        "phone_number": customer.phone_number
    }

    def convert_books_to_json(self,book):
        return_book= {
                "id": book.id,
                "title": book.title,
                "author_name": book.author_name,
                "publisher": book.publisher,
                "year_of_publish": book.year_of_publish,
                "borrowed": book.borrowed,
                "borrowed_by": book.borrowed_by
            }
        
        return return_book
    

    def save_books(self , book):
        try:
            with open("library_book.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        jsonBook=self.convert_books_to_json(book)
        data.append(jsonBook)
        with open("library_book.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Books saved successfully!")

    
    def save_customers(self , customer):
        try:
            with open("customers.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        jsonCustomer = self.conver_customer_to_json(customer)
        data.append(jsonCustomer)
        with open("customers.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Customers saved successfully!")

    def load_customers(self):
        try:
            with open('customers.json' , 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def load_books(self): # returns list of dicts
        #C:\Back-end Star union\library_books.json
        try:
            with open('library_book.json' , 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []


    def run (self):
        while True:
            print("\n===== Library Management System =====")
            print("1. Add Book")
            print("2. Add Customer")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. Display Available Books")
            print("6. Exit")

            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                try:
                    books = self.load_books()
                    id = books[-1]['id'] + 1 if books else 1
                    title = input("Enter book title: ")
                    author = input("Enter author name: ")
                    publisher = input("Enter publisher: ")
                    year = int(input("Enter year of publish: "))
                    # books_to_save = self.add_book(Book(id, title, author, publisher, year))
                    self.add_book(Book(id, title, author, publisher, year))
                    # self.save_books(books_to_save)

                except ValueError:
                    print("Invalid input, please try again.")
            elif choice == '2':
                try:
                    custs = self.load_customers()
                    id = custs[-1]['id']+1 if custs else 1
                    name = input("Enter customer name: ")
                    phone = input("Enter phone number: ")
                    self.add_customer(User(id, name, phone))

                except ValueError:      
                    print("Invalid input, please try again.")

            elif choice == "3":
                book_title = input("Enter book title: ")
                customer_name = input("Enter customer name: ")
                customer_id = int(input("Enter customer ID: "))
                self.borrow_book(book_title, customer_name, customer_id)
            elif choice == "4":
                book_title = input("Enter book title: ")
                self.return_book(book_title)

            elif choice == "5":
                self.display_available_books()

            elif choice == "6":
                print("Exiting system... Goodbye 👋")
                break

            else:
                print("Invalid choice, please select from the menu.")


if __name__ == '__main__':
    library = Library()
    library.run()