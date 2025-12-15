from storage import Storage, NotFoundError
from interface import Interface
from book import Book
from user import User


class LMS:
    def __init__(
        self,
        storage: Storage = None,
        interface: Interface = None,
    ):
        self.storage: Storage = storage if storage else Storage()
        self.interface: Interface = interface if interface else Interface()

    def run(self):
        self.storage.init()
        self.interface.init()

        while True:
            opt = self.interface.run_main_menu()

            if opt == 1:
                self.choose_user_action()
            elif opt == 2:
                self.choose_book_action()
            elif opt == 3:
                self.choose_borrowing_action()
            else:
                raise Exception(f"Unsupported option {opt}")

    def choose_user_action(self):
        opt = self.interface.run_user_menu()

        if opt == 1:
            self.read_user()
        elif opt == 2:
            self.update_user()
        elif opt == 3:
            self.create_user()
        elif opt == 4:
            self.delete_user()
        elif opt == 5:
            self.show_users()
        else:
            raise Exception(f"Unsupported option {opt}")

    # LMS CRUD functions are different from Storage CRUD function as the first shows output too.
    def read_user(self):
        id = self.interface.run_read_user_id()
        try:
            user = self.storage.read_user(id)
        except NotFoundError as e:
            self.interface.show_error_message(e.message)
        else:
            self.interface.show_obj(user)

    def update_user(self):
        id = self.interface.run_read_user_id()
        try:
            user = self.storage.read_user(id)
        except NotFoundError as e:
            self.interface.show_error_message(e.message)   
        else: 
            data = self.interface.run_update_user_menu()
            user.update(*data)
            self.storage.update_user(user)
            self.interface.show_user_updated_successfully()
    
    def create_user(self):
        data = self.interface.run_create_user_menu()
        user = User(None, *data, [])
        self.storage.create_user(user)
        self.interface.show_user_created_successfully()
    
    def delete_user(self):
        id = self.interface.run_read_user_id()
        try:
            self.storage.delete_user(id)
        except NotFoundError as e:
            self.interface.show_error_message(e.message)
        else:
            self.interface.show_user_deleted_successfully()
    
    def show_users(self):
        ids = sorted(self.storage.get_users_ids())
        self.interface.show_users(ids)
              
    def choose_book_action(self):
        opt = self.interface.run_book_menu()

        if opt == 1:
            self.read_book()
        elif opt == 2:
            self.update_book()
        elif opt == 3:
            self.create_book()
        elif opt == 4:
            self.delete_book()
        elif opt == 5:
            self.show_books()
        else:
            raise Exception(f"Unsupported option {opt}")

    def read_book(self):
        id = self.interface.run_read_book_id()
        try:
            book = self.storage.read_book(id)
        except NotFoundError as e:
            self.interface.show_error_message(e.message)
        else:
            self.interface.show_obj(book)

    def update_book(self):
        id = self.interface.run_read_book_id()
        try:
            book = self.storage.read_book(id)
        except NotFoundError as e:
            self.interface.show_error_message(e.message)
        else:
            data = self.interface.run_update_book_menu()
            book.update(*data)
            self.storage.update_book(book)
            self.interface.show_book_updated_successfully()
    
    def create_book(self):
        data = self.interface.run_create_book_menu()
        book = Book(None, *data)
        self.storage.create_book(book)
        self.interface.show_book_created_successfully()
    
    def delete_book(self):
        id = self.interface.run_read_book_id()
        try:
            self.storage.delete_book(id)
        except NotFoundError as e:
            self.interface.show_error_message(e.message)
        else:
            self.interface.show_book_deleted_successfully()

    def show_books(self):
        ids = sorted(self.storage.get_books_ids())
        self.interface.show_books(ids)

    def choose_borrowing_action(self):
        opt = self.interface.run_borrowing_menu()
        if opt == 1:
            self.borrow_book()
        elif opt == 2:
            self.return_book()
        elif opt == 3:
            self.show_borrowings()
        else:
            raise Exception(f"Unsupported option {opt}")
    
    def borrow_book(self):
        uid = self.interface.run_read_user_id()
        try:
            user = self.storage.read_user(uid)
        except NotFoundError as e:
            self.interface.show_error_message(e.message)
            return
        
        bid = self.interface.run_read_book_id()
        try:
            self.storage.ensure_book_exists(bid)
        except NotFoundError as e:
            self.interface.show_error_message(e.message)
            return
        
        if bid in user.borrowings:
            self.interface.show_user_already_borrowed_book()
            return
        user.borrowings.append(bid)
        
        self.storage.update_user(user)
        self.interface.show_user_borrowed_book_successfully()
    
    def return_book(self):
        uid = self.interface.run_read_user_id()
        try:
            user = self.storage.read_user(uid)
        except NotFoundError as e:
            self.interface.show_error_message(e.message)
            return
        
        bid = self.interface.run_read_book_id()
        try:
            self.storage.ensure_book_exists(bid)
        except NotFoundError as e:
            self.interface.show_error_message(e.message)
            return
                
        try:
            user.borrowings.remove(bid)
        except:
            self.interface.show_error_user_havent_borrowed_this_book()        
        
        self.storage.update_user(user)
        self.interface.show_user_returned_book_successfully() 
    
    def show_borrowings(self):
        id = self.interface.run_read_user_id()
        try:
            user = self.storage.read_user(id)
        except NotFoundError as e:
            self.interface.show_error_message(e.message)
            return
        
        self.interface.show_user_borrowings(id, user.borrowings)
        