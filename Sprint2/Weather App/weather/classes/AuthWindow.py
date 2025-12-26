import tkinter as tk
from tkinter import ttk, messagebox

from .Auth import Auth

class AuthWindow:
    def __init__(self, on_auth_success):
        self.on_auth_success = on_auth_success
        self.auth = Auth()
        
        self.root = tk.Tk()
        self.root.title("Weather App - Login/Register")
        self.root.geometry("300x300")
        self.root.resizable(False, False)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill='both', expand=True)
        
        # Create login frame
        self.login_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.login_frame, text='Login')
        
        # Create register frame
        self.register_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.register_frame, text='Register')
        
        self.setup_login_frame()
        self.setup_register_frame()
        
        self.root.mainloop()
    
    def setup_login_frame(self):
        # Username
        ttk.Label(self.login_frame, text="Username:").pack(pady=(10, 0))
        self.login_username = ttk.Entry(self.login_frame, width=25)
        self.login_username.pack(pady=5)
        
        # Password
        ttk.Label(self.login_frame, text="Password:").pack(pady=(10, 0))
        self.login_password = ttk.Entry(self.login_frame, width=25, show="*")
        self.login_password.pack(pady=5)
        
        # Login button
        ttk.Button(
            self.login_frame, 
            text="Login", 
            command=self.handle_login,
            width=20
        ).pack(pady=20)
    
    def setup_register_frame(self):
        # Username
        ttk.Label(self.register_frame, text="Username:").pack(pady=(10, 0))
        self.reg_username = ttk.Entry(self.register_frame, width=25)
        self.reg_username.pack(pady=5)
        
        # Password
        ttk.Label(self.register_frame, text="Password:").pack(pady=(10, 0))
        self.reg_password = ttk.Entry(self.register_frame, width=25, show="*")
        self.reg_password.pack(pady=5)
        
        # Confirm Password
        ttk.Label(self.register_frame, text="Confirm Password:").pack(pady=(10, 0))
        self.reg_confirm_password = ttk.Entry(self.register_frame, width=25, show="*")
        self.reg_confirm_password.pack(pady=5)
        
        # Register button
        ttk.Button(
            self.register_frame, 
            text="Register", 
            command=self.handle_register,
            width=20
        ).pack(pady=20)
    
    def handle_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        success, message = self.auth.login(username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.root.destroy()
            self.on_auth_success(username)
        else:
            messagebox.showerror("Error", message)
    
    def handle_register(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm_password = self.reg_confirm_password.get()
        
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        success, message = self.auth.register(username, password)
        if success:
            messagebox.showinfo("Success", message)
            # Switch to login tab after successful registration
            self.notebook.select(0)
            self.login_username.delete(0, tk.END)
            self.login_username.insert(0, username)
            self.login_password.focus()
        else:
            messagebox.showerror("Error", message)
