import customtkinter as ctk
from gui.login import LoginFrame
from gui.dashboard import DashboardFrame
from engin.db import init_db

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Order Management System")
        self.geometry("1200x800")
        
        # Initialize DB
        init_db()

        self.current_user = None

        # Grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.login_frame = LoginFrame(self, login_callback=self.login_success)
        self.dashboard_frame = None

        self.show_login()

    def show_login(self):
        if self.dashboard_frame:
            self.dashboard_frame.grid_forget()
        self.login_frame.grid(row=0, column=0, sticky="nsew")

    def login_success(self, user):
        self.current_user = user
        self.login_frame.grid_forget()
        self.dashboard_frame = DashboardFrame(self, user=self.current_user, logout_callback=self.logout)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

    def logout(self):
        self.current_user = None
        self.show_login()
