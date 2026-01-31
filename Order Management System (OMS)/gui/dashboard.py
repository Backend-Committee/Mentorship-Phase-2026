import customtkinter as ctk
from tkinter import messagebox
import bcrypt
from engin.db import SessionLocal
from gui.pages.selling import SellingPage
from gui.pages.analysis import AnalysisPage
from gui.pages.admin import AdminPage

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, user, logout_callback):
        super().__init__(master)
        self.user = user
        self.logout_callback = logout_callback

        # Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text=f"Welcome\n{user.username}", font=("Roboto", 20, "bold"))
        self.logo_label.pack(pady=20, padx=10)

        self.btn_selling = ctk.CTkButton(self.sidebar, text="Selling", command=lambda: self.show_frame("selling"))
        self.btn_selling.pack(pady=10, padx=20)

        self.btn_analysis = ctk.CTkButton(self.sidebar, text="Analysis", command=lambda: self.show_frame("analysis"))
        self.btn_analysis.pack(pady=10, padx=20)

        if self.user.role in ["admin", "super_admin"]:
            self.btn_admin = ctk.CTkButton(self.sidebar, text="Admin Panel", command=lambda: self.show_frame("admin"))
            self.btn_admin.pack(pady=10, padx=20)

        self.btn_logout = ctk.CTkButton(self.sidebar, text="Logout", fg_color="red", command=self.logout_callback)
        self.btn_logout.pack(pady=20, padx=20, side="bottom")

        self.btn_change_pw = ctk.CTkButton(self.sidebar, text="Change Password", fg_color="gray", command=self.change_password_dialog)
        self.btn_change_pw.pack(pady=10, padx=20, side="bottom")

        # Main Content Area
        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_rowconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.init_frames()
        self.show_frame("selling")

    def init_frames(self):
        self.frames["selling"] = SellingPage(self.main_area, self.user)
        self.frames["analysis"] = AnalysisPage(self.main_area, self.user)
        if self.user.role in ["admin", "super_admin"]:
            self.frames["admin"] = AdminPage(self.main_area, self.user)

    def show_frame(self, name):
        if name == "selling":
             if "selling" in self.frames:
                 self.frames["selling"].load_products()
        
        for frame in self.frames.values():
            frame.grid_forget()
        self.frames[name].grid(row=0, column=0, sticky="nsew")

    def change_password_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Change Password")
        dialog.geometry("300x280")
        # Make the dialog modal
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Current Password").pack(pady=5)
        old_pw = ctk.CTkEntry(dialog, show="*")
        old_pw.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="New Password").pack(pady=5)
        new_pw = ctk.CTkEntry(dialog, show="*")
        new_pw.pack(pady=5)
        
        def save():
            old = old_pw.get()
            new = new_pw.get()
            
            if not old or not new:
                messagebox.showerror("Error", "All fields required")
                return

            # Verify old password
            # self.user.password is likely a hashed string.
            try:
                if not bcrypt.checkpw(old.encode('utf-8'), self.user.password.encode('utf-8')):
                     messagebox.showerror("Error", "Incorrect old password")
                     return
            except Exception as e:
                # Fallback if password isn't hashed properly or legacy
                if old != self.user.password:
                     messagebox.showerror("Error", "Incorrect old password")
                     return

            new_hashed = bcrypt.hashpw(new.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            db = SessionLocal()
            # We need to get the class to query. 
            # Assuming self.user is an instance of User
            UserClass = type(self.user)
            u = db.query(UserClass).get(self.user.id)
            if u:
                u.password = new_hashed
                db.commit()
                self.user.password = new_hashed # Update local reference
                messagebox.showinfo("Success", "Password changed successfully")
                dialog.destroy()
            else:
                 messagebox.showerror("Error", "User record not found")
            db.close()

        ctk.CTkButton(dialog, text="Save", command=save).pack(pady=20)
