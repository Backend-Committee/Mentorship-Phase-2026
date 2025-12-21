import json
from email_validator import validate_email,EmailNotValidError

from User import User


class AuthSystem:
    def __init__(self):
        self.users = []
        self.loadData()
    def loadData(self,filename='users.json'):
        try:
           with open(filename,'r') as file:
               if file.read().strip():
                   file.seek(0)
                   data = json.load(file)
                   self.users = [User(**u) for u in data['users']]
        except FileNotFoundError:
            print("Data file not found. Starting with empty auth system.")
        except json.JSONDecodeError:
            print("Invalid JSON format in data file. Starting with empty auth system.")
    def saveData(self,filename='users.json'):
        with open(filename,'w') as file:
            data = {
                'users' : [ u.toDict() for u in self.users]
            }
            json.dump(data,file,indent=4)
    def saveUser(self,username,email,password):
        new_user = User(username,email,password)
        self.users.append(new_user)
        self.saveData()
        print("User registered successfully.")
    def authenticateEmail(self,email,):
        if any(u.email == email for u in self.users):
            return True
        return False
    def authanticatePassword(self,email,password):
        if any(u.email == email and u.password == password for u in self.users):
            return True
        return False
    def loginUser(self,email,password):
        if not self.authenticateEmail(email):
            print("Email not found.")
            return False
        if not self.authanticatePassword(email,password):
            print("Incorrect password.")
            return False
        print("Login successful.")
        return True
    def registerUser(self,username,email,password):
        if self.authenticateEmail(email):
            print("Email already registered.")
            return False
        self.saveUser(username,email,password)
        return True
    def validateEmail(self,email):
        try:
            valid = validate_email(email)
            return True
        except EmailNotValidError as e:
            print(str(e))
            return False



