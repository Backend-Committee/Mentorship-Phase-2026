from sys import stderr, stdin


class Interface:
    def init(self):
        print("WELCOME TO THE LMS!\n")

    def run_main_menu(self):
        print()
        print(
            "1- User management\n2- Book management\n3- Borrowing and returning books\n"
        )
        return self._get_opt(1, 3)

    def run_user_menu(self):
        print()
        print(
            "1- Read user data\n2- Update user data\n3- Create user\n4- Delete user\n5- Show all users ids"
        )
        return self._get_opt(1, 5)

    def run_read_user_id(self) -> int:
        return self._get_int("User id: ")

    def run_update_user_menu(self) -> dict:
        print("Update user (leave blank to keep current value)")
        name = input("New name: ").strip()
        email = input("New email: ").strip()
        return name, email

    def run_create_user_menu(self) -> dict:
        # TODO: validation logic so that name and email can't be empty
        print("Create new user")
        name = input("Name: ").strip()
        email = input("Email: ").strip()
        return name, email

    def run_book_menu(self):
        print()
        print("1- Read book data\n2- Update book data\n3- Create book\n4- Delete book\n5- Show all books ids")
        return self._get_opt(1, 5)

    def run_read_book_id(self) -> int:
        return self._get_int("Book id: ")

    def run_update_book_menu(self) -> tuple:
        print("Update book (leave blank to keep current value)")
        title = input("New title: ").strip()
        author = input("New author: ").strip()
        try:
            pub_date = int(input("New publication year: ").strip())
        except:
            pub_date = None
        return title, author, pub_date

    def run_create_book_menu(self) -> tuple:
        print("Create new book")
        title = input("Title: ").strip()
        author = input("Author: ").strip()
        pub_date = self._get_int("Publication year: ")
        return title, author, pub_date

    def run_borrowing_menu(self) -> int:
        print()
        print("1- Borrow a book\n2- Return a book\n3- Show user borrowed books")
        return self._get_opt(1, 3)

    def run_borrow_menu_get_ids(self) -> dict:
        print("Borrow/return - provide ids")
        uid = self._get_int("User id: ")
        bid = self._get_int("Book id: ")
        return {"user_id": uid, "book_id": bid}
    
    
    def show_obj(self, obj):
        print("\n" + str(obj) + "\n")
        self._wait_for_enter()

    def show_error_message(self, message):
        print("\nERROR: " + str(message) + "\n", file=stderr)
        self._wait_for_enter()

    def show_user_updated_successfully(self):
        self.show_success_message(f"User updated successfully")

    def show_user_created_successfully(self):
        self.show_success_message(f"User created successfully")
    
    def show_users(self, ids):
        print("\nUsers ids is", ids, "\n")
        self._wait_for_enter()

    def show_books(self, ids):
        print("\nBooks ids is", ids, "\n")
        self._wait_for_enter()

    def show_user_deleted_successfully(self):
        self.show_success_message(f"User deleted successfully")

    def show_book_updated_successfully(self):
        self.show_success_message(f"Book updated successfully")

    def show_book_created_successfully(self):
        self.show_success_message(f"Book created successfully")

    def show_book_deleted_successfully(self):
        self.show_success_message(f"Book deleted successfully")

    def show_success_message(self, message):
        print("\n" + str(message) + "\n")

    def show_user_already_borrowed_book(self):
        self.show_error_message("User already borrowed this book")

    def show_user_borrowed_book_successfully(self):
        self.show_success_message("Book borrowed successfully")

    def show_error_user_havent_borrowed_this_book(self):
        self.show_error_message("User hasn't borrowed this book")

    def show_user_returned_book_successfully(self):
        self.show_success_message("Book returned successfully")
    
    def show_user_borrowings(self, id, user_borrowings):
        print(f"User with id {id} has borrowed books with ids {user_borrowings}")

    def _get_opt(self, start, end) -> int:
        while True:
            try:
                print()
                opt = int(input("> "))
            except ValueError:
                ...
            else:
                if opt >= start and opt <= end:
                    return opt

            print("This is not a valid option, please try again!", file=stderr)

    def _get_int(self, prompt) -> int:
        while True:
            try:
                print()
                opt = int(input(prompt + " "))
                return opt
            except ValueError:
                print("Please enter a valid integer.", file=stderr)

    def _wait_for_enter(self):
        # TODO: turn off command line echo here.
        print("PRESS ENTER TO CONTINUE", end="", flush=True)
        while stdin.read(1) != "\n":
            ...
