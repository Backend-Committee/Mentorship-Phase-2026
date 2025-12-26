import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from .Weather import Weather
from .Auth import Auth

class GUI():
    def __init__(self, root, username) -> None:
        self.root = root
        self.username = username
        self.auth = Auth()
        self.dropdown_id = None
        self.options = self.getCities()
        
        # Set window properties
        self.root.title(f"Weather App - Welcome, {self.username}")
        self.root.geometry('400x400')
        
        # User info frame
        user_frame = ttk.Frame(self.root)
        user_frame.pack(fill='x', padx=10, pady=5)
        
        # Display current user
        ttk.Label(user_frame, text=f"Logged in as: {self.username}").pack(side='left')
        
        # Logout button
        ttk.Button(
            user_frame, 
            text="Logout",
            command=self.logout,
            style='Accent.TButton'
        ).pack(side='right')
        
        # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        # City selection frame
        wrapper = ttk.LabelFrame(main_frame, text="Search City", padding=10)
        wrapper.pack(fill='x', pady=5)
        
        # City entry with dropdown
        entry_frame = ttk.Frame(wrapper)
        entry_frame.pack(fill='x')
        
        self.entry = ttk.Entry(entry_frame, width=30)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown) 
        self.entry.pack(side='left', expand=True, fill='x')
        
        # Dropdown icon/button
        try:
            self.icon = ImageTk.PhotoImage(Image.open("dropdown_arrow.png").resize((16,16)))
            ttk.Button(entry_frame, image=self.icon, command=self.show_dropdown).pack(side='left', padx=5)
        except:
            ttk.Button(entry_frame, text="▼", command=self.show_dropdown, width=2).pack(side='left', padx=5)
        
        # Add to favorites button
        ttk.Button(
            wrapper, 
            text="Add to Favorites",
            command=self.add_to_favorites,
            style='Accent.TButton'
        ).pack(pady=(10, 0), fill='x')
        
        # Create a Listbox widget for the dropdown menu
        self.listbox = tk.Listbox(main_frame, height=5, width=40)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        
        # Load user's favorite cities
        self.load_favorite_cities()
        
        # Weather info frame
        self.weather_frame = ttk.LabelFrame(main_frame, text="Weather Information", padding=10)
        self.weather_frame.pack(fill='both', expand=True, pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var,
            relief='sunken', 
            anchor='center',
            padding=5
        )
        self.status_bar.pack(side='bottom', fill='x')
        self.status_var.set(f"Welcome, {self.username}! Search for a city to see the weather.")
        
        # Configure styles
        self.configure_styles()
        
        # Button to get weather
        button = ttk.Button(
            main_frame, 
            text="Get Weather",
            command=self.getWeatherBtn,
            style='Accent.TButton'
        )
        button.pack(padx=20, pady=20)
        

        #Tempreture 
        self.tempLabel = tk.Label(root, text="Temperature: ")
        self.tempLabel.pack()
        #Humidity
        self.humLabel = tk.Label(root, text="Humidity: ")
        self.humLabel.pack()


        #Wind Speed
        self.windLabel = tk.Label(root, text="Wind Speed: ")
        self.windLabel.pack()
        #Pressure
        self.pressureLabel = tk.Label(root, text="Pressure: ")
        self.pressureLabel.pack()
        #Precipitation
        self.precipititionLabel = tk.Label(root, text="Precipitation: ")
        self.precipititionLabel.pack()

        root.mainloop()
    def getCities(self):
        # Check if we already have the cities cached
        if not hasattr(self, '_cities_cache'):
            try:
                # Fetch cities from API only once
                response = requests.get('https://countriesnow.space/api/v0.1/countries')
                if response.status_code == 200:
                    cities = []
                    countries = response.json().get("data", [])
                    for country in countries:
                        cities.extend(country.get("cities", []))
                    # Cache the sorted list
                    self._cities_cache = sorted(set(cities))  # Remove duplicates and sort
                    return self._cities_cache
                else:
                    # Return a default list if API fails
                    return self._get_default_cities()
            except Exception as e:
                print(f"Error fetching cities: {e}")
                return self._get_default_cities()
        return self._cities_cache

    def _get_default_cities(self):
        """Return a default list of major cities if API fails"""
        return [
            "New York", "London", "Tokyo", "Paris", "Dubai",
            "Singapore", "Barcelona", "Rome", "Istanbul", "Moscow",
            "Beijing", "Sydney", "Cairo", "Rio de Janeiro", "Toronto"
        ]


    def getWeatherBtn(self):
        w = Weather()
        entryText = self.entry.get()
        if entryText:
            w.setCity(entryText)
        weather = w.getWeather()
        temp_celsius = weather["main"]["temp"] - 273.15  # Convert from Kelvin to Celsius
        self.tempLabel.config(text=f'Temperature: {temp_celsius:.1f}°C')
        self.pressureLabel.config(text=f'Pressure: {weather["main"]["pressure"]} hPa')
        self.humLabel.config(text=f'Humidity: {weather["main"]["humidity"]}%')
        self.windLabel.config(text=f'Wind Speed: {weather["wind"]["speed"]} m/s')
        self.precipititionLabel.config(text=f'Conditions: {weather["weather"][0]["main"]}')


    def on_entry_key(self, event):
        typed_value = event.widget.get().strip().lower()
        if not typed_value:
            self.listbox.delete(0, tk.END)
            return
        
        # Get cities from cache or API
        cities = self.getCities()
        
        # Use list comprehension for faster filtering
        filtered = [city for city in cities if city.lower().startswith(typed_value)]
        
        # Update the listbox
        self.listbox.delete(0, tk.END)
        for city in filtered[:50]:  # Limit to 50 results for performance
            self.listbox.insert(tk.END, city)
        
        self.show_dropdown()

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_option = self.listbox.get(selected_index)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_option)

    def show_dropdown(self, event=None):
        self.listbox.place(in_=self.entry, x=0, rely=1, relwidth=1.0, anchor="nw")
        self.listbox.lift()

        # Show dropdown for 2 seconds
        if self.dropdown_id: # Cancel any old events
            self.listbox.after_cancel(self.dropdown_id)
        self.dropdown_id = self.listbox.after(2000, self.hide_dropdown)

    def hide_dropdown(self):
        self.listbox.place_forget()

    def configure_styles(self):
        """Configure ttk styles for the application"""
        style = ttk.Style()
        style.configure('Accent.TButton', 
                      font=('Arial', 10, 'bold'),
                      padding=5)
        
        # Configure the main window background
        self.root.configure(bg='#f0f0f0')
    
    def load_favorite_cities(self):
        """Load user's favorite cities into the dropdown"""
        favorites = self.auth.get_user_cities(self.username)
        if favorites:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, favorites[0])  # Load first favorite by default
            self.status_var.set(f"Loaded {len(favorites)} favorite cities")
    
    def add_to_favorites(self):
        """Add current city to user's favorites"""
        city = self.entry.get().strip()
        if not city:
            self.status_var.set("Please select a city first")
            return
            
        if city in self.options:
            if self.auth.add_city(self.username, city):
                self.status_var.set(f"Added {city} to favorites")
            else:
                self.status_var.set(f"{city} is already in your favorites")
        else:
            self.status_var.set("Please select a valid city")
    
    def logout(self):
        """Handle user logout"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            # Restart the application to show login window
            from main import on_auth_success
            root = tk.Tk()
            auth_window = AuthWindow(on_auth_success)
    
    def clear_weather_display(self):
        """Clear all weather information"""
        self.tempLabel.config(text="Temperature: ")
        self.pressureLabel.config(text="Pressure: ")
        self.humLabel.config(text="Humidity: ")
        self.windLabel.config(text="Wind Speed: ")
        self.precipititionLabel.config(text="Conditions: ")