# library_system.py
import json
class Book:
    def __init__(self, book_id, title, author, category, pages):
        self.id = book_id
        self.title = title.lower()
        self.author = author
        self.category = category
        self.pages = pages
        self.status = True

    def summary(self):
        return f"{self.title} by {self.author} — {self.pages} pages [{self.category}]"

    def to_json(self):
        return {
            "ID": self.id,
            "title": self.title,
            "author": self.author,
            "category": self.category,
            "pages": self.pages,
            "status" : self.status
        }


class User:
    def __init__(self, user_id, name, email, phone):
        self.id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_books = []

    def info(self):
        return f"{self.name} ({self.email})"

    def add_book(self, book):
        self.borrowed_books.append(book)

    def remove_book(self, book):
        self.borrowed_books = [b for b in self.borrowed_books if b.id != book.id]

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "borrowedBooks": 
            [
                {
                    "id": b.id,
                    "title": b.title,
                    "author": b.author,
                    "category": b.category,
                    "pages": b.pages
                }
                for b in self.borrowed_books
            ]
        }


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def show_books(self):
        return [b.summary() for b in self.books]

    def search_book_and_borrow(self, title, user):
        book = next((b for b in self.books if b.title == title and b.status), None)
        if book:
            book.status = False
            user.add_book(book)
            return True
        return False

    def return_book(self, book_id, user):
        book = next((b for b in self.books if b.id == book_id), None)
        if book:
            book.status = True
            user.remove_book(book)
            return True
        return False

    def borrow_book_Proccess(self):
        print("Start Borrow Process")

        user_id = int(input("Enter user id: "))
        user = next((u for u in self.users if u.id == user_id), None)
        if not user:
            print("User not found!")
            return

        title = input("Enter book title: ").lower()
        ok = self.search_book_and_borrow(title, user)
        if not ok:
            print("Book not available or not found!")

        print("\nUser borrowed books:")
        if user.borrowed_books:
            print("\n".join(b.summary() for b in user.borrowed_books))
        else:
            print("None")

    def to_json(self):
        return {
            "name": self.name,
            "books": [b.to_json() for b in self.books],
            "users": [u.to_json() for u in self.users]
        }
    
    def save_to_file(self, filename="library_data.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_json(), f, indent=2, ensure_ascii=False)
        print(f"Saved to {filename}")

    
    def menu(self):
        while True:
            print("\n===== Library Menu =====")
            print("1) Borrow a book")
            print("2) Return a book")
            print("3) Show all books")
            print("4) Exit")

            choice = input("Choose (1-4): ").strip()

            if choice == "1":
                self.borrow_book_Proccess()
            elif choice == "2":
                try:
                    user_id = int(input("Enter user id: "))
                except ValueError:
                    print("Invalid user id!")
                    continue

                user = next((u for u in self.users if u.id == user_id), None)
                if not user:
                    print("User not found!")
                    continue

                try:
                    book_id = int(input("Enter book id to return: "))
                except ValueError:
                    print("Invalid book id!")
                    continue

                ok = self.return_book(book_id, user)
                if not ok:
                    print("Book not found!")
                else:
                    print("Book returned successfully!")

            elif choice == "3":
                books = self.show_books()
                if books:
                    print("\n".join(books))
                else:
                    print("No books!")

            elif choice == "4":
                print("Goodbye!")
                break

            else:
                print("Invalid choice, try again.")


def main():
    lib = Library("My Library")

    # add books
    lib.add_book(Book(1, "Clean Code", "Robert Martin", "Software", 464))
    lib.add_book(Book(2, "OOP", "Novel", "SOLID", 328))

    # add users
    u1 = User(10, "Ahmed", "ahmedshalhadad1@gmail.com", "01091575793")
    lib.add_user(u1)

    # show library JSON (before borrow)
    print("=== Library JSON (Before Borrow) ===")
    print(json.dumps(lib.to_json(), indent=2, ensure_ascii=False))


    # borrow via User
    lib.menu()

    lib.save_to_file()

    # print("\n=== Library JSON (After Borrow) ===")
    # print(json.dumps(lib.to_json(), indent=2, ensure_ascii=False))


    # # test return book
    # lib.return_book(1, u1)

    # print("\n=== Library JSON (After Return Test) ===")
    # print(json.dumps(lib.to_json(), indent=2, ensure_ascii=False))




if __name__ == '__main__':
    main()
