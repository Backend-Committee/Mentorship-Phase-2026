"""
    Weather display window showing current, hourly, and weekly forecasts.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from models.Weather import Weather
from GUI.styles import Theme
from datetime import datetime

class WeatherWindow:
    """Window for displaying weather information."""
    
    def __init__(self, root, username, logout_callback):
        self.root = root
        self.username = username
        self.logout_callback = logout_callback
        self.weather = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the weather UI."""
        # Top frame with user info and logout
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        user_label = ttk.Label(top_frame, text=f"Welcome, {self.username}", style="Subtitle.TLabel")
        user_label.pack(side=tk.LEFT)
        
        logout_btn = ttk.Button(top_frame, text="Logout", command=self.logout, style="Secondary.TButton")
        logout_btn.pack(side=tk.RIGHT)
        
        # Search frame
        search_frame = ttk.Frame(self.root, style="Card.TFrame", padding="15")
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(search_frame, text="Search Location", style="Card.TLabel").pack(side=tk.LEFT, padx=(0, 10))
        
        self.location_var = tk.StringVar()
        location_entry = ttk.Entry(search_frame, textvariable=self.location_var, width=30)
        location_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        search_btn = ttk.Button(search_frame, text="Search", command=self.search_weather)
        search_btn.pack(side=tk.LEFT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Current weather tab
        self.current_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.current_frame, text="Current")
        
        # Hourly forecast tab
        self.hourly_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.hourly_frame, text="Hourly (24h)")
        
        # Weekly forecast tab
        self.weekly_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.weekly_frame, text="Weekly")
        
        # History tab
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="History")
        
        self.show_history()
    
    def search_weather(self):
        """Search for weather in a location."""
        location = self.location_var.get().strip()
        
        if not location:
            messagebox.showerror("Error", "Please enter a location")
            return
        
        # Show loading message (optional, can be annoying if fast)
        # messagebox.showinfo("Loading", "Fetching weather data...")
        
        try:
            self.weather = Weather()
            weather_data = self.weather.get_all_weather(location)
            
            if not weather_data:
                messagebox.showerror("Error", "Location not found or API error")
                return
            
            # Save to history using the model
            self.weather.save_to_history(self.username)
            
            # Display current weather
            self.show_current_weather()
            self.show_hourly_forecast()
            self.show_weekly_forecast()
            self.show_history()
            
            # messagebox.showinfo("Success", f"Weather data loaded for {location}")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching weather: {str(e)}")
    
    def show_current_weather(self):
        """Display current weather information."""
        # Clear frame
        for widget in self.current_frame.winfo_children():
            widget.destroy()
        
        if not self.weather or not self.weather.current_weather:
            ttk.Label(self.current_frame, text="No data available. Search for a location.").pack(pady=20)
            return
        
        current = self.weather.current_weather
        
        # Main Info Card
        main_card = ttk.Frame(self.current_frame, style="Card.TFrame", padding="20")
        main_card.pack(fill=tk.X, pady=(0, 20))
        
        # Location & Date
        header_frame = ttk.Frame(main_card, style="Card.TFrame")
        header_frame.pack(fill=tk.X)
        
        ttk.Label(header_frame, text=self.weather.location, style="CardTitle.TLabel", font=Theme.H2).pack(side=tk.LEFT)
        ttk.Label(header_frame, text=datetime.now().strftime("%A, %d %B"), style="Card.TLabel").pack(side=tk.RIGHT)
        
        # Temp & Desc
        content_frame = ttk.Frame(main_card, style="Card.TFrame")
        content_frame.pack(fill=tk.X, pady=20)
        
        temp_frame = ttk.Frame(content_frame, style="Card.TFrame")
        temp_frame.pack(side=tk.LEFT)
        
        ttk.Label(temp_frame, text=f"{int(current['temp'])}°", font=(Theme.FONT_FAMILY, 64, "bold"), style="Card.TLabel").pack(side=tk.LEFT)
        
        desc_frame = ttk.Frame(content_frame, style="Card.TFrame")
        desc_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(desc_frame, text=current['description'].title(), font=Theme.H3, style="Card.TLabel").pack(anchor="w")
        ttk.Label(desc_frame, text=f"Feels like {int(current['feels_like'])}°", style="Card.TLabel").pack(anchor="w")
        
        # Grid Details
        details_frame = ttk.Frame(self.current_frame)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        details = [
            ("Humidity", f"{current['humidity']}%"),
            ("Wind Speed", f"{current['wind_speed']} m/s"),
            ("Pressure", f"{current['pressure']} hPa"),
            ("Cloudiness", f"{current['clouds']}%"),
            ("Min Temp", f"{current['temp_min']}°"),
            ("Max Temp", f"{current['temp_max']}°"),
        ]
        
        for i, (label, value) in enumerate(details):
            card = ttk.Frame(details_frame, style="Card.TFrame", padding="15")
            card.grid(row=i//2, column=i%2, sticky="nsew", padx=5, pady=5)
            
            ttk.Label(card, text=label, style="Subtitle.TLabel", font=Theme.SMALL).pack(anchor="w")
            ttk.Label(card, text=value, style="Card.TLabel", font=Theme.H3).pack(anchor="w")
            
        details_frame.columnconfigure(0, weight=1)
        details_frame.columnconfigure(1, weight=1)

    def _create_scrollable_frame(self, parent):
        """Helper to create a scrollable frame."""
        canvas = tk.Canvas(parent, bg=Theme.BG_PRIMARY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=parent.winfo_width())
        
        # Update width on resize
        def on_canvas_configure(event):
            canvas.itemconfig(canvas.find_all()[0], width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return scrollable_frame

    def show_hourly_forecast(self):
        """Display hourly forecast."""
        for widget in self.hourly_frame.winfo_children():
            widget.destroy()
        
        if not self.weather or not self.weather.hourly_forecast:
            ttk.Label(self.hourly_frame, text="No data available").pack(pady=20)
            return
        
        scrollable_frame = self._create_scrollable_frame(self.hourly_frame)
        
        for hourly in self.weather.hourly_forecast:
            row = ttk.Frame(scrollable_frame, style="Card.TFrame", padding="15")
            row.pack(fill=tk.X, pady=5, padx=5)
            
            # Time
            ttk.Label(row, text=hourly['time'], style="CardTitle.TLabel", width=10).pack(side=tk.LEFT)
            
            # Temp
            ttk.Label(row, text=f"{int(hourly['temp'])}°C", style="Card.TLabel", font=Theme.H3, width=8).pack(side=tk.LEFT)
            
            # Desc
            ttk.Label(row, text=hourly['description'].title(), style="Card.TLabel").pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Wind/Humidity
            info = f"Wind: {hourly['wind_speed']}m/s  |  Hum: {hourly['humidity']}%"
            ttk.Label(row, text=info, style="Subtitle.TLabel", font=Theme.SMALL).pack(side=tk.RIGHT)

    def show_weekly_forecast(self):
        """Display weekly forecast."""
        for widget in self.weekly_frame.winfo_children():
            widget.destroy()
        
        if not self.weather or not self.weather.weekly_forecast:
            ttk.Label(self.weekly_frame, text="No data available").pack(pady=20)
            return
        
        scrollable_frame = self._create_scrollable_frame(self.weekly_frame)
        
        for daily in self.weather.weekly_forecast:
            row = ttk.Frame(scrollable_frame, style="Card.TFrame", padding="15")
            row.pack(fill=tk.X, pady=5, padx=5)
            
            # Date
            ttk.Label(row, text=daily['date'], style="CardTitle.TLabel", width=15).pack(side=tk.LEFT)
            
            # Temp Range
            temp_range = f"{int(daily['temp_min'])}° / {int(daily['temp_max'])}°"
            ttk.Label(row, text=temp_range, style="Card.TLabel", font=Theme.H3, width=12).pack(side=tk.LEFT)
            
            # Desc
            ttk.Label(row, text=daily['description'].title(), style="Card.TLabel").pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Extra Info
            info = f"Wind: {daily['wind_speed']:.1f}m/s"
            ttk.Label(row, text=info, style="Subtitle.TLabel", font=Theme.SMALL).pack(side=tk.RIGHT)

    def show_history(self):
        """Display search history."""
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        history = Weather.get_user_weather_history(self.username)
        
        if not history:
            ttk.Label(self.history_frame, text="No search history yet.", style="Subtitle.TLabel").pack(pady=20)
            return
        
        scrollable_frame = self._create_scrollable_frame(self.history_frame)
        
        for weather_item in history:
            row = ttk.Frame(scrollable_frame, style="Card.TFrame", padding="15")
            row.pack(fill=tk.X, pady=5, padx=5)
            
            # Location & Time
            info_frame = ttk.Frame(row, style="Card.TFrame")
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            ttk.Label(info_frame, text=weather_item.location, style="CardTitle.TLabel").pack(anchor="w")
            ttk.Label(info_frame, text=weather_item.search_timestamp or "Unknown Date", style="Subtitle.TLabel", font=Theme.SMALL).pack(anchor="w")
            
            # Temp if available
            if weather_item.current_weather:
                temp = f"{int(weather_item.current_weather['temp'])}°C"
                ttk.Label(row, text=temp, style="Card.TLabel", font=Theme.H3).pack(side=tk.RIGHT)

    def logout(self):
        """Handle logout."""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.logout_callback()
