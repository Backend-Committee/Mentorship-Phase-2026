import tkinter as tk
from classes.GUI import GUI
from classes.AuthWindow import AuthWindow

def on_auth_success(username):
    # This function is called after successful authentication
    root = tk.Tk()
    app = GUI(root, username)
    root.mainloop()

if __name__ == "__main__":
    # Show authentication window first
    auth_window = AuthWindow(on_auth_success)