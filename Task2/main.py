from Auth_System import AuthSystem

def main_menu():
    auth_system = AuthSystem()

    while True:
        print("\n--- Auth System Menu ---")
        print("1. Register User")
        print("2. Login User")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            if auth_system.validateEmail(email):
                auth_system.registerUser(username, email, password)
        elif choice == "2":
            email = input("Enter email: ")
            password = input("Enter password: ")
            auth_system.loginUser(email, password)
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

main_menu()