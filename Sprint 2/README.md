# University Search System with Authentication

A simple Python console application that allows users to **sign up, log in**, and **search for universities** using the Hipolabs Universities API.

---

## 📌 Project Overview

- Users can **create an account** and **log in**.
- After login, users can **search universities** by country and name (supports partial & case-insensitive matches).
- Displays:
  - University name
  - Country
  - Website

---

## 🛠️ How It Works

1. **Authentication**  
   - User signs up with username, email, and password.
   - Users log in with username and password.
   - User data is stored in `users.json`.

2. **University Search**  
   - Uses `requests` to call `http://universities.hipolabs.com/search`.
   - Filters universities by `country` and `name`.
   - Prints the first matching university's details.

---

## ▶️ Sample Run

Sign up

Login

Exit
Choose an option: 2
Enter your username: zeyad
Enter your password: 1234
Login successful
Access granted
Enter the country you search for: Egypt
Enter the name of University: Cairo
University: Cairo University
Country: Egypt
Website: ['http://www.cu.edu.eg/']


---

## ⚠️ Notes

- Passwords are stored in plain text (for learning purposes only).
- University search is **case-insensitive** and supports **partial name matches**.
