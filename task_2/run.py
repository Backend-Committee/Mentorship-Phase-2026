from auth_system import AuthSystem
from auth_system.user import User
from auth_system.validation import ValidationError
from utils import get_opt
import os
from analyzer import Analyzer
import json
import tkinter as tk
from PIL import Image, ImageTk

STORAGE_PATH = "storage"
CACHE_PATH = "cache"


ROUND_TO_NAME = {
    1: "Final",
    2: "3rd Place Final",
    3: "Semi-finals",
    4: "Quarter-finals",
    5: "Round of 16",
}


def register():
    while True:
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")

        user = User(username, email, password)
        try:
            auth_system.register(user)
        except ValidationError as e:
            print("SORRY, TRY AGAIN!")
            print(e.message)
            print()
        else:
            print()
            print("ACCOUNT CREATED SUCCESSFULLY!")
            print("run the program again to login")
            print()
            exit(1)


def login():
    username_or_email = input("Username or email: ")
    password = input("Password: ")

    if auth_system.login(username_or_email, password):
        print()
        print("LOGGED IN SUCCESSFULLY!")
        print()
    else:
        print()
        print("INVALID, SO GOODBYE!")
        print()
        exit(1)


def show_player(name, country, rating, photo, country_logo, round):
    # ---------------- Window ----------------
    root = tk.Tk()
    root.title("Best player")
    root.geometry("400x500")
    root.configure(bg="#111827")  # dark background

    # ---------------- Card ----------------
    card = tk.Frame(root, bg="#1f2937", bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=440)

    # ---------------- Title ----------------
    tk.Label(
        card,
        text=f"Best player at {round}",
        bg="#1f2937",
        fg="#38bdf8",
        font=("Segoe UI", 18, "bold"),
    ).pack(pady=15)

    # ---------------- Images ----------------
    img = Image.open(photo)
    player_img = ImageTk.PhotoImage(img)
    
    img = Image.open(country_logo)
    country_img = ImageTk.PhotoImage(img)

    img_frame = tk.Frame(card, bg="#1f2937")
    img_frame.pack(pady=10)

    tk.Label(img_frame, image=player_img, bg="#1f2937").grid(row=0, column=0, padx=15)
    tk.Label(img_frame, image=country_img, bg="#1f2937").grid(row=0, column=1, padx=15)

    # ---------------- Info ----------------
    def info(label, value):
        f = tk.Frame(card, bg="#1f2937")
        f.pack(anchor="w", padx=30, pady=5)

        tk.Label(
            f, text=label + ":", bg="#1f2937", fg="#9ca3af", font=("Segoe UI", 11)
        ).pack(side="left")

        tk.Label(
            f, text=value, bg="#1f2937", fg="#f9fafb", font=("Segoe UI", 11, "bold")
        ).pack(side="left", padx=6)

    info("Name", name)
    info("Country", country)

    # ---------------- Match Rating (ONLY THIS MATCH) ----------------
    rating_frame = tk.Frame(card, bg="#111827")
    rating_frame.pack(pady=25)

    tk.Label(
        rating_frame,
        text="Match Rating",
        bg="#111827",
        fg="#facc15",
        font=("Segoe UI", 12),
    ).pack()

    tk.Label(
        rating_frame,
        text=rating,
        bg="#111827",
        fg="#facc15",
        font=("Segoe UI", 42, "bold"),
    ).pack()

    # ---------------- Footer ----------------
    tk.Label(
        card,
        text=f"AFCON 2023 • {round}",
        bg="#1f2937",
        fg="#6b7280",
        font=("Segoe UI", 10),
    ).pack(side="bottom", pady=12)
    
    root.focus_force()
    card.focus_force()
    root.mainloop()


if __name__ == "__main__":
    print("WELCOME ?, COMO VAS ?")
    print()
    print("1- Register")
    print("2- Login")
    print()
    opt = get_opt(1, 2)
    print()

    os.makedirs(STORAGE_PATH, exist_ok=True)
    auth_system = AuthSystem(STORAGE_PATH)
    if opt == 1:
        register()
    elif opt == 2:
        login()
    else:
        raise Exception()

    print("Now, choose which round you want the best player from")
    print("for money issues this work for africa cup 2023 instead of africa cup 2025")
    for round_num, round_name in ROUND_TO_NAME.items():
        print(f'{round_num}- "{round_name}"')
    print()
    opt = get_opt(1, 8)
    print()
    round = ROUND_TO_NAME[opt]

    os.makedirs(CACHE_PATH, exist_ok=True)
    analyzer = Analyzer(dir_path=CACHE_PATH)
    best_player = analyzer.get_best_player(round)
    photo = analyzer.save_player_image(best_player["photo"])
    country_logo = analyzer.save_country_logo(best_player["country_logo"])
    
    print("THE BEST PLAYER")
    print(json.dumps(best_player, indent=2))
    analyzer.close()
    show_player(
        best_player["name"],
        best_player["country"],
        best_player["rating"],
        photo,
        country_logo,
        round
    )
