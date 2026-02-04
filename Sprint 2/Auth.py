import json

def check_user(username, password, file_obj):
    file_obj.seek(0)
    try:
        users = json.load(file_obj)
    except json.JSONDecodeError:
        return False

    for user in users:
        if user["username"] == username and user["password"] == password:
            return True

    return False


def Login (file_obj):
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    if check_user(username , password , file_obj):
        print('Login successful')
        return True
    else:
        print('Invalid username or password')
        return False


def sign_up(file_obj):
    username = input("Enter a username: ")
    Email = input("Enter your Email: ")
    password = input("Enter a password: ")

    file_obj.seek(0)
    file_obj.truncate()
    try:
        users = json.load(file_obj)
    except json.JSONDecodeError:
        users = []

    # prevent duplicates
    for user in users:
        if user["username"].lower() == username.lower():
            print("Username already exists")
            return False

    users.append({
        "username": username,
        "email": Email,
        "password": password
    })

    json.dump(users, file_obj, indent=4)

    print("Sign up successful")
    return True


def run_auth_system(file_obj):
    while True:
        print("\n1. Sign up")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            sign_up(file_obj)

            return

        elif choice == "2":
            success = Login(file_obj)
            if success:
                print("Access granted")
                return

        else:
            print("Invalid choice")