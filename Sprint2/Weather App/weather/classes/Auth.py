import json
import os
import hashlib
from tkinter import messagebox

class Auth:
    def __init__(self, db_file='users.json'):
        self.db_file = db_file
        self.users = {}
        self.load_users()
    
    def hash_password(self, password):
        """Hash the password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    self.users = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.users = {}
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def register(self, username, password):
        """Register a new user"""
        if username in self.users:
            return False, "Username already exists"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        self.users[username] = {
            'password': self.hash_password(password),
            'cities': []  # Store user's favorite cities
        }
        self.save_users()
        return True, "Registration successful"
    
    def login(self, username, password):
        """Authenticate a user"""
        if username not in self.users:
            return False, "Invalid username or password"
        
        if self.users[username]['password'] != self.hash_password(password):
            return False, "Invalid username or password"
        
        return True, "Login successful"
    
    def get_user_cities(self, username):
        """Get user's favorite cities"""
        if username in self.users:
            return self.users[username].get('cities', [])
        return []
    
    def add_city(self, username, city):
        """Add a city to user's favorites"""
        if username in self.users:
            if 'cities' not in self.users[username]:
                self.users[username]['cities'] = []
            if city not in self.users[username]['cities']:
                self.users[username]['cities'].append(city)
                self.save_users()
                return True
        return False
