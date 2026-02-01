import os

from InquirerPy.base.control import Choice
from pyfiglet import figlet_format
from termcolor import cprint

from database_conf import DatabaseManager
from features.account.repo import AccountRepo
from features.account.screen import (
    AccountsMenuScreen,
    CreateAccountScreen,
    ExpenseScreen,
    IncomeScreen,
    TransactionScreen,
    TransferScreen,
)
from features.account.service import AccountService
from features.auth.repo import AuthInfoRepo
from features.auth.screen import AuthMenuScreen, LoginScreen, RegisterScreen
from features.auth.service import AuthService
from features.user.model import User
from features.user.repo import UserRepo
from features.user.screen import (
    ChangeDisplayNameScreen,
    DeleteMyAccountScreen,
    ProfileMenuScreen,
    ProfileScreen,
)
from features.user.service import UserService


def clear():
    """Cross-platform clear screen — works on Windows and Linux/Mac."""
    os.system("cls" if os.name == "nt" else "clear")


class AppController:
    def __init__(self):
        # Bootstrap dependencies
        self.db = DatabaseManager()
        self.user_repo = UserRepo(self.db.conn)
        self.user_service = UserService(self.user_repo)
        self.account_repo = AccountRepo(self.db.conn)
        self.account_service = AccountService(self.account_repo)
        self.auth_repo = AuthInfoRepo(self.db.conn)
        self.auth_service = AuthService(self.auth_repo, self.user_repo)

        self.current_user = None

        # Screen registry — maps route strings to screen classes
        self.screens = {
            "main_menu": self._main_menu,
            "profile_menu": lambda: ProfileMenuScreen(
                self.user_service, self.current_user
            ),
            "profile": lambda: ProfileScreen(self.user_service, self.current_user),
            "change_display_name": lambda: ChangeDisplayNameScreen(
                self.user_service, self.current_user
            ),
            "delete_my_account": lambda: DeleteMyAccountScreen(
                self.user_service, self.current_user
            ),
            "accounts": lambda: AccountsMenuScreen(
                self.account_service, self.current_user
            ),
            "create_account": lambda: CreateAccountScreen(
                self.account_service, self.current_user
            ),
            "transaction": lambda: TransactionScreen(
                self.account_service, self.current_user
            ),
            "expense": lambda: ExpenseScreen(
                self.account_service, self.current_user, self.send_message
            ),
            "income": lambda: IncomeScreen(
                self.account_service, self.current_user, self.send_message
            ),
            "trasnfer": lambda: TransferScreen(
                self.account_service, self.current_user, self.send_message
            ),
            "auth": lambda: AuthMenuScreen(),
            "login": lambda: LoginScreen(
                self.auth_service, self.onLoginSuccess, self.send_message
            ),
            "register": lambda: RegisterScreen(
                self.auth_service, self.onLoginSuccess, self.send_message
            ),
        }

        self.route = "main_menu"
        self.message = "Hey from expense star"

    def _print_art(
        self,
        text: str,
        font: str = "starwars",
        text_color: str = "black",
        bold: bool = True,
        border: bool = True,
    ):
        """
        Prints stylish ASCII art banner to the terminal.
        """

        art = figlet_format(text, font=font)
        attrs = ["bold"] if bold else []

        if border:
            lines = art.splitlines()
            width = max(len(line) for line in lines)
            border_line = "-" * (width + 4)

            cprint(border_line, text_color, attrs=attrs)
            for line in lines:
                padded = f"| {line.ljust(width)} |"
                cprint(padded, text_color, attrs=attrs)
            cprint(border_line, text_color, attrs=attrs)
        else:
            cprint(art, text_color, attrs=attrs)

    def onLoginSuccess(self, user: User) -> None:
        self.current_user = user

    def send_message(self, message: str) -> None:
        self.message = message

    def _simulate_login(self):
        """Temporary: simulates a logged-in user until auth is implemented."""
        from features.user.model import User

        # Hardcoded placeholder — swap with auth service login later
        return User(id=1, display_name="TestUser", auth_id=1)

    def _main_menu(self):
        """Root menu screen — will expand as more features are added."""
        from InquirerPy import inquirer

        return inquirer.select(
            message="ExpenseStar",
            choices=[
                Choice("profile", name="Your Profile"),
                Choice("accounts", name="Accounts"),
                Choice("exit", name="Exit"),
            ],
        ).execute()

    def run(self):
        """Main loop — resolves the current route, renders the screen, and navigates."""

        if self.current_user is None:
            self.route = "auth"

        while self.route != "exit":
            clear()
            self._print_art(
                text="Expense Star",
                font="slant",
                text_color="white",
                border=True,
            )
            print(self.message)
            self.message = ""

            screen_factory = self.screens.get(self.route)

            if screen_factory is None:
                print(
                    f"\n✘ Unknown route: '{self.route}'. Falling back to main menu.\n"
                )
                self.route = "main_menu"
                continue

            # main_menu is a method, others are lambdas that return screen instances
            if self.route == "main_menu":
                self.route = screen_factory()
            elif self.route == "back":
                self.route = "main_menu"
            else:
                screen = screen_factory()
                self.route = screen.render()

        clear()
        print("\n  Goodbye!\n")
