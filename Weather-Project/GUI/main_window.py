"""
    Main GUI window for the Weather Application.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import requests
from datetime import datetime
from models.Weather import Weather
from models.User import User

from GUI.auth_window import AuthWindow
from GUI.weather_window import WeatherWindow
from GUI.styles import setup_styles, Theme

class MainWindow:
    """Main application window."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("450x600")
        # self.root.resizable(False, False) # Allow resizing for better UX
        
        self.current_user = None
        self.weather = None
        
        # Configure style
        self.style = setup_styles(self.root)
        
        self.show_auth_window()
    
    def show_auth_window(self):
        """Show authentication window."""
        # Clear root
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.auth_window = AuthWindow(self.root, self.on_auth_success)
    
    def on_auth_success(self, username):
        """Callback when user successfully authenticates."""
        self.current_user = username
        self.show_weather_window()
    
    def show_weather_window(self):
        """Show weather window after authentication."""
        # Clear root
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("800x700")
        self.weather_window = WeatherWindow(self.root, self.current_user, self.on_logout)
    
    def on_logout(self):
        """Callback when user logs out."""
        self.current_user = None
        self.root.geometry("400x500")
        self.show_auth_window()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
