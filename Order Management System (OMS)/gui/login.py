import customtkinter as ctk
from tkinter import messagebox
import bcrypt
from engin.db import SessionLocal
from models.User import user as User

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, login_callback):
        super().__init__(master)
        self.login_callback = login_callback

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.label = ctk.CTkLabel(self, text="OMS Login", font=("Roboto", 24))
        self.label.grid(row=1, column=1, pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.grid(row=2, column=1, pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.grid(row=3, column=1, pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_event)
        self.login_button.grid(row=4, column=1, pady=20)

    def login_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db = SessionLocal()
        user_record = db.query(User).filter_by(username=username).first()
        db.close()

        if user_record and bcrypt.checkpw(password.encode('utf-8'), user_record.password.encode('utf-8')):
            self.login_callback(user_record)
        else:
            messagebox.showerror("Login Error", "Invalid username or password")
