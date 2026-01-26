from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

from urllib.parse import quote_plus

connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=ZANATY;"
    "Database=stardb1;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

params = quote_plus(connection_string)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

base = declarative_base()
class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
def create_user(name, email):
    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()
    print("User created")
def select_user(id=None):
    user = session.query(User).filter(User.id == id).first()
    return user
def select_users():
    users = session.query(User).all()
    return users
def update_user(id, name=None, email=None):
    user = session.query(User).filter(User.id == id).first()
    if user:
        if name:
            user.name = name
        if email:
            user.email = email
        session.commit()
        print("User updated")
    else:
        print("User not found")
def delete_user(id):
    user = session.query(User).filter(User.id == id).first()
    if user:
        session.delete(user)
        session.commit()
        print("User deleted")
    else:
        print("User not found")

# --- CLI menu ---------------------------------------------------------------
def print_menu():
    print("\nSimple CRUD menu:")
    print("1) Create user")
    print("2) List users")
    print("3) Get user by id")
    print("4) Update user")
    print("5) Delete user")
    print("6) Exit")

def input_int(prompt):
    while True:
        val = input(prompt).strip()
        if val == "":
            return None
        try:
            return int(val)
        except ValueError:
            print("Please enter a valid integer.")

def main():
    try:
        while True:
            print_menu()
            choice = input("Choose an option: ").strip()
            if choice == "1":
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                if name and email:
                    create_user(name, email)
                else:
                    print("Name and email required.")
            elif choice == "2":
                users = select_users()
                if users:
                    for u in users:
                        print(f"{u.id}: {u.name} <{u.email}>")
                else:
                    print("No users found.")
            elif choice == "3":
                uid = input_int("User id: ")
                if uid is None:
                    print("ID required.")
                else:
                    u = select_user(uid)
                    if u:
                        print(f"{u.id}: {u.name} <{u.email}>")
                    else:
                        print("User not found.")
            elif choice == "4":
                uid = input_int("User id: ")
                if uid is None:
                    print("ID required.")
                else:
                    name = input("New name (leave blank to keep): ").strip() or None
                    email = input("New email (leave blank to keep): ").strip() or None
                    update_user(uid, name=name, email=email)
            elif choice == "5":
                uid = input_int("User id: ")
                if uid is None:
                    print("ID required.")
                else:
                    delete_user(uid)
            elif choice == "6" or choice.lower() in ("q","quit","exit"):
                print("Exiting.")
                break
            else:
                print("Invalid choice.")
    finally:
        try:
            session.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
