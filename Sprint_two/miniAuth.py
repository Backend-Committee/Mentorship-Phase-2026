from dataclasses import dataclass
from dataclasses import asdict
import re
import json
from pathlib import Path

@dataclass
class User:
    username: str
    password: str
    email: str


class MiniAuth:
    def __init__(self):
        # ensure DB path and load index
        self.db_path = Path(__file__).parent / "JSONFiles" / "DB.JSON"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self.db_path.write_text("[]", encoding="utf-8")
        self.loadIndex()
        pass
    
    def loadIndex(self):
        try:
            text = self.db_path.read_text(encoding="utf-8").strip()
            if not text:
                data = []
            else:
                # try parsing JSON content (could be list, dict, or a JSON string)
                data = json.loads(text) if isinstance(text, str) else text
        except (json.JSONDecodeError, ValueError):
            data = []
        # normalize data to a list of user dicts
        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list):
            data = []
        # build index only from dict entries that have an "email" key
        self.Index = {u["email"]: u for u in data if isinstance(u, dict) and "email" in u}

    def updateFile(self):
        with self.db_path.open("w", encoding="utf-8") as file:
            json.dump(list(self.Index.values()), file, indent=4)
        print("User registered successfully.")
    
    def validate_user(self, email: str) -> bool:
        return email in self.Index
    
    def register_user(self, username: str, password: str, email: str):
        if not self.validate_user(email):
            user = User(username, password, email)
            user_data = asdict(user)
            self.Index[email] = user_data
            return self.updateFile()  # removed extra argument
        else:
            print("This email is already registered.")

    def login_user(self, email: str, password: str):
        if self.validate_user(email):
            if self.Index[email]["password"] == password:
                return print("Login successful.\nWelcome back, " + self.Index[email]["username"] + "!")
            else:
                print("!!Incorrect password.")
                return print("Login failed.")
        else:
            return print("!!Email not found. Please register first.")

def CheckEmail(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def CheckPassword(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True
def main():
    auth = MiniAuth()
    print("\n\n=============================================")
    print("================= Hi There! =================")
    print("=============================================\n\n")
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if not CheckPassword(password):
                print("!!Password must be at least 8 characters long,\ncontain uppercase and lowercase letters,\nand include at least one digit.\nPlease try again.")
                continue
            email = input("Enter email: ")
            if not CheckEmail(email):
                print("!!Invalid email format. Please try again.")
                continue
            auth.register_user(username, password, email)
        elif choice == '2':
            email = input("Enter email: ")
            password = input("Enter password: ")
            auth.login_user(email, password)
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
    # Example usage:
    # auth.register_user("testuser", "password123", "testuser@example.com")
    # auth.login_user("testuser@example.com", "password123")

