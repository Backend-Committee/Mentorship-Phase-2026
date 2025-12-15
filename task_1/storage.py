import json
from collections import deque
from user import User
from book import Book
import os

# TODO: consider implementing a cache so for example model instances may be returned again and again without doing that much work.
# TODO: consider implementing a file pool so that you can reuse the same file handles again and again.


class Storage:
    def init(self):
        self.create_files()
        self.init_users()
        self.init_books()
    
    def create_files(self):
        if not os.path.exists("users"):
            os.mkdir("./users")
        if not os.path.exists("books"):
            os.mkdir("./books")
        if not os.path.exists("users/meta.json"):
            with open("users/meta.json", "x") as f:
                json.dump({"next_id": 1, "ids":[]}, f)
        if not os.path.exists("books/meta.json"):
            with open("books/meta.json", "x") as f:
                json.dump({"next_id": 1, "ids":[]}, f)
            
        
    def init_users(self):
        with open("users/meta.json") as f:
            # users_meta.ids is an array that we keep just for fast serialization
            # while users_ids_set is kept for fast checking of existence of an id
            self.users_meta = json.load(f)
            self.users_ids_set = set(self.users_meta["ids"])

    def init_books(self):
        with open("books/meta.json") as f:
            # books_meta.ids is an array that we keep just for fast serialization
            # while books_ids_set is kept for fast checking of existence of an id
            self.books_meta = json.load(f)
            self.books_ids_set = set(self.books_meta["ids"])

    def init_borrows(): ...

    def ensure_user_exists(self, id):
        if id not in self.users_ids_set:
            raise NotFoundError(message=f"user with id {id} doesn't exist!")

    def read_user(self, id):
        self.ensure_user_exists(id)

        with open(f"users/{id}.json") as f:
            return User(id=id, **json.load(f))

    def update_user(self, user: User):
        with open(f"users/{user.id}.json", "w") as f:
            json.dump(user.serialize(), f)

    def create_user(self, user):
        user.id = self.users_meta["next_id"]
        self.users_ids_set.add(user.id)
        self.users_meta["ids"].append(user.id)
        self.users_meta["next_id"] += 1

        with open("users/meta.json", "w") as f:
            json.dump(self.users_meta, f)

        with open(f"users/{user.id}.json", "w") as f:
            json.dump(user.serialize(), f)

    def delete_user(self, id):
        self.ensure_user_exists(id)

        os.remove(f"users/{id}.json")
        
        self.users_meta["ids"].remove(id)
        self.users_ids_set.remove(id)
        with open("users/meta.json", "w") as f:
            json.dump(self.users_meta, f)
        
    def get_users_ids(self):
        return self.users_meta['ids']

    def get_books_ids(self):
        return self.books_meta['ids']

    def ensure_book_exists(self, id):
        if id not in self.books_ids_set:
            raise NotFoundError(message=f"book with id {id} doesn't exist!")

    def read_book(self, id):
        self.ensure_book_exists(id)

        with open(f"books/{id}.json") as f:
            return Book(id=id, **json.load(f))

    def update_book(self, book: Book):
        with open(f"books/{book.id}.json", "w") as f:
            json.dump(book.serialize(), f)

    def create_book(self, book):
        book.id = self.books_meta["next_id"]
        self.books_ids_set.add(book.id)
        self.books_meta["ids"].append(book.id)
        self.books_meta["next_id"] += 1

        with open("books/meta.json", "w") as f:
            json.dump(self.books_meta, f)

        with open(f"books/{book.id}.json", "w") as f:
            json.dump(book.serialize(), f)

    def delete_book(self, id):
        self.ensure_book_exists(id)

        os.remove(f"books/{id}.json")
        
        self.books_meta["ids"].remove(id)
        self.books_ids_set.remove(id)
        with open("books/meta.json", "w") as f:
            json.dump(self.books_meta, f)


class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__()
