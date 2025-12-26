# Weather App Project

A modern, Python-based desktop application that provides real-time weather information, hourly forecasts, and weekly outlooks using the Open-Meteo API. The application features a user-friendly GUI with a dark theme, user authentication, and search history.

## Features

- **User Authentication**: Secure login and registration system using `bcrypt` for password hashing.
- **Real-time Weather**: Get current weather conditions (Temperature, Humidity, Wind Speed, etc.) for any location.
- **Detailed Forecasts**:
  - **Hourly Forecast**: 24-hour outlook with 3-hour intervals.
  - **Weekly Forecast**: 5-day weather prediction including min/max temperatures.
- **Search History**: Automatically saves your recent searches for quick access.
- **Modern GUI**: Clean, dark-themed interface built with `tkinter` and `ttk`.
- **No API Key Required**: Powered by the Open-Meteo API.

## Technologies Used

- **Language**: Python 3.x
- **GUI Framework**: Tkinter (ttk)
- **API**: [Open-Meteo API](https://open-meteo.com/)
- **Libraries**:
  - `requests`: For API calls.
  - `bcrypt`: For secure password handling.
  - `Pillow`: For image/icon processing.

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Weather-Project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python App.py
   ```

## Project Structure

```
Weather-Project/
├── App.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── GUI/                    # Graphical User Interface modules
│   ├── auth_window.py      # Login/Signup screens
│   ├── main_window.py      # Main container window
│   ├── weather_window.py   # Weather dashboard
│   └── styles.py           # Theme and style configuration
├── models/                 # Data models
│   ├── User.py             # User management
│   ├── Weather.py          # Weather data model
│   └── Base_model.py       # Base class for models
├── Weather/                # Weather service logic
│   └── logic.py            # Open-Meteo API integration
└── Storage/                # Data persistence
    └── storage.json        # JSON file for storing user/history data
```

## Contributor

- **Name**: Mahmoud Ahmed Ibrahim Adam
- **Email**: mahmoudadam5555@gmail.com 
- **Github User**: [mahmoud-5555](https://github.com/mahmoud-5555)
- **LinkedIn**: [Mahmoud Adam](https://www.linkedin.com/in/mahmoud-adam-bb3056248/)

