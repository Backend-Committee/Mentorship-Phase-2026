from auth_system import AuthSystem
from auth_system.user import User
from auth_system.validation import ValidationError
from utils import get_opt
import os
from analyzer import Analyzer
import json

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
    print("THE BEST PLAYER")
    print(json.dumps(best_player, indent=2))