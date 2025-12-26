"""
    Centralized styles and theme configuration for the application.
"""

import tkinter as tk
from tkinter import ttk

class Theme:
    """Theme colors and fonts."""
    
    # Colors (Dark Theme)
    BG_PRIMARY = "#1e1e1e"      # Dark gray background
    BG_SECONDARY = "#252526"    # Slightly lighter gray for cards/panels
    BG_TERTIARY = "#333333"     # Input fields, etc.
    
    FG_PRIMARY = "#ffffff"      # White text
    FG_SECONDARY = "#cccccc"    # Light gray text
    
    ACCENT = "#007acc"          # Blue accent
    ACCENT_HOVER = "#0098ff"    # Lighter blue for hover
    
    ERROR = "#f44336"           # Red for errors
    SUCCESS = "#4caf50"         # Green for success
    
    # Fonts (Initialized in setup_styles)
    FONT_FAMILY = "Arial"
    
    H1 = ("Arial", 24, "bold")
    H2 = ("Arial", 18, "bold")
    H3 = ("Arial", 14, "bold")
    BODY = ("Arial", 11)
    BODY_BOLD = ("Arial", 11, "bold")
    SMALL = ("Arial", 9)

def setup_styles(root):
    """Configure ttk styles."""
    # Detect font
    try:
        available_fonts = root.tk.call("font", "families")
        if "Segoe UI" in available_fonts:
            Theme.FONT_FAMILY = "Segoe UI"
        elif "Helvetica" in available_fonts:
            Theme.FONT_FAMILY = "Helvetica"
    except:
        pass
        
    # Update font constants
    Theme.H1 = (Theme.FONT_FAMILY, 24, "bold")
    Theme.H2 = (Theme.FONT_FAMILY, 18, "bold")
    Theme.H3 = (Theme.FONT_FAMILY, 14, "bold")
    Theme.BODY = (Theme.FONT_FAMILY, 11)
    Theme.BODY_BOLD = (Theme.FONT_FAMILY, 11, "bold")
    Theme.SMALL = (Theme.FONT_FAMILY, 9)

    style = ttk.Style(root)
    
    # Use 'clam' as base for better customization support
    style.theme_use('clam')
    
    # Configure generic TFrame
    style.configure("TFrame", background=Theme.BG_PRIMARY)
    
    # Configure Main Window
    root.configure(bg=Theme.BG_PRIMARY)
    
    # Labels
    style.configure("TLabel", 
                   background=Theme.BG_PRIMARY, 
                   foreground=Theme.FG_PRIMARY,
                   font=Theme.BODY)
    
    style.configure("Title.TLabel", 
                   font=Theme.H1,
                   foreground=Theme.ACCENT)
                   
    style.configure("Subtitle.TLabel", 
                   font=Theme.H2,
                   foreground=Theme.FG_SECONDARY)
                   
    style.configure("Card.TLabel",
                   background=Theme.BG_SECONDARY,
                   foreground=Theme.FG_PRIMARY,
                   font=Theme.BODY)

    style.configure("CardTitle.TLabel",
                   background=Theme.BG_SECONDARY,
                   foreground=Theme.ACCENT,
                   font=Theme.H3)
    
    # Buttons
    style.configure("TButton",
                   background=Theme.ACCENT,
                   foreground=Theme.FG_PRIMARY,
                   borderwidth=0,
                   focuscolor=Theme.ACCENT,
                   font=Theme.BODY_BOLD,
                   padding=(10, 5))
                   
    style.map("TButton",
              background=[('active', Theme.ACCENT_HOVER), ('pressed', Theme.ACCENT)],
              foreground=[('active', Theme.FG_PRIMARY)])
              
    style.configure("Secondary.TButton",
                   background=Theme.BG_TERTIARY,
                   foreground=Theme.FG_PRIMARY)
                   
    style.map("Secondary.TButton",
              background=[('active', '#4d4d4d')])

    # Entry
    style.configure("TEntry",
                   fieldbackground=Theme.BG_TERTIARY,
                   foreground=Theme.FG_PRIMARY,
                   insertcolor=Theme.FG_PRIMARY,
                   borderwidth=0,
                   padding=5)
                   
    # Notebook (Tabs)
    style.configure("TNotebook",
                   background=Theme.BG_PRIMARY,
                   borderwidth=0)
                   
    style.configure("TNotebook.Tab",
                   background=Theme.BG_SECONDARY,
                   foreground=Theme.FG_SECONDARY,
                   padding=(15, 5),
                   borderwidth=0)
                   
    style.map("TNotebook.Tab",
              background=[('selected', Theme.ACCENT)],
              foreground=[('selected', Theme.FG_PRIMARY)])
              
    # Card Frame (Custom style for cards)
    style.configure("Card.TFrame", background=Theme.BG_SECONDARY, relief="flat")
    
    return style
