"""
    Authentication window for user login and registration.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from models.User import User
from GUI.styles import Theme

class AuthWindow:
    """Authentication window for login and signup."""
    
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.current_user = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the authentication UI."""
        # Center container
        container = ttk.Frame(self.root)
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Card Frame
        card = ttk.Frame(container, style="Card.TFrame", padding="30")
        card.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = ttk.Label(card, text="Weather App", style="Title.TLabel")
        title.pack(pady=(0, 10))
        
        subtitle = ttk.Label(card, text="Welcome Back", style="Subtitle.TLabel")
        subtitle.pack(pady=(0, 20))
        
        # Username
        ttk.Label(card, text="Username", style="Card.TLabel").pack(anchor="w", pady=(5, 0))
        self.username_var = tk.StringVar()
        username_entry = ttk.Entry(card, textvariable=self.username_var, width=35)
        username_entry.pack(pady=(5, 15))
        
        # Password
        ttk.Label(card, text="Password", style="Card.TLabel").pack(anchor="w", pady=(5, 0))
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(card, textvariable=self.password_var, width=35, show="*")
        password_entry.pack(pady=(5, 15))
        
        # Email (for signup)
        ttk.Label(card, text="Email (Optional for Login)", style="Card.TLabel").pack(anchor="w", pady=(5, 0))
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(card, textvariable=self.email_var, width=35)
        email_entry.pack(pady=(5, 20))
        
        # Buttons
        login_btn = ttk.Button(card, text="Login", command=self.login, width=35)
        login_btn.pack(pady=(0, 10))
        
        signup_btn = ttk.Button(card, text="Create Account", command=self.signup, style="Secondary.TButton", width=35)
        signup_btn.pack(pady=(0, 10))
        
        # Demo button
        demo_btn = ttk.Button(card, text="Try Demo", command=self.demo_login, style="Secondary.TButton", width=35)
        demo_btn.pack(pady=(0, 5))
    
    def login(self):
        """Handle login."""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        # Get user from storage
        user = User.get_user_by_username(username)
        
        if user is None:
            messagebox.showerror("Error", "User does not exist")
            return
        
        if user.check_password(password):
            # messagebox.showinfo("Success", f"Welcome {username}!")
            self.callback(username)
            self.current_user = user
        else:
            messagebox.showerror("Error", "Invalid password")
    
    def signup(self):
        """Handle signup."""
        username = self.username_var.get().strip()
        password = self.password_var.get()
        email = self.email_var.get().strip()
        
        if not username or not password or not email:
            messagebox.showerror("Error", "Please fill all fields (including Email for signup)")
            return
        
        if User.get_user_by_username(username) is not None:
            messagebox.showerror("Error", "Username already exists")
            return
        
        if '@' not in email:
            messagebox.showerror("Error", "Invalid email address")
            return
        
        # Create new user
        user = User(username=username, email=email, password=password)
        User.save()
        
        messagebox.showinfo("Success", "Account created successfully! Please login.")
        
        # Clear fields
        self.username_var.set("")
        self.password_var.set("")
        self.email_var.set("")
    
    def demo_login(self):
        """Quick demo login."""
        demo_user = "demo"
        demo_password = "demo123"
        demo_email = "demo@example.com"
        
        # Check if demo user exists, if not create it
        user = User.get_user_by_username(demo_user)
        if user is None:
            user = User(username=demo_user, email=demo_email, password=demo_password)
            User.save()
        
        # Populate fields and login
        self.username_var.set(demo_user)
        self.password_var.set(demo_password)
        self.login()
