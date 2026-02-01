import re

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from features.auth.service import AuthService


class AuthMenuScreen:
    """Entry point before login — routes to register or login."""

    def render(self) -> str:
        return inquirer.select(
            message="ExpenseStar - Authentication",
            choices=[
                Choice("login", name="Login"),
                Choice("register", name="Register"),
                Choice("exit", name="Exit"),
            ],
        ).execute()


class LoginScreen:
    """Collects username + password, verifies credentials via AuthService."""

    def __init__(
        self, service: AuthService, on_success: callable, send_message: callable
    ):
        self.service = service
        self.on_success = on_success  # callback to store the logged-in user
        self.send_message = send_message

    def render(self) -> str:
        username = inquirer.text(
            message="Username",
        ).execute()

        password = inquirer.secret(
            message="Password",
        ).execute()

        try:
            user = self.service.login(username, password)
            self.on_success(user)  # hand the user up to the controller
            self.send_message(f"\nWelcome back, {user.display_name}!\n")
            return "main_menu"
        except (ValueError, LookupError) as e:
            self.send_message(f"\n{e}\n")
            return "auth"


class RegisterScreen:
    """Collects registration details, creates auth + user profile."""

    def __init__(
        self, service: AuthService, on_success: callable, send_message: callable
    ):
        self.service = service
        self.on_success = on_success  # callback to store the logged-in user
        self.send_message = send_message

    def validate_email(answers, current):
        """Validate an email address using regex."""
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, current))

    def render(self) -> str:
        print("Register: ")

        username = inquirer.text(
            message="Username",
        ).execute()

        email = inquirer.text(
            message="Email",
            validate=self.validate_email,
            invalid_message="Please enter a valid email",
        ).execute()

        password = inquirer.secret(
            message="Password",
        ).execute()

        confirm_password = inquirer.secret(
            message="Confirm Password",
        ).execute()

        if password != confirm_password:
            self.send_message("\n✘ Passwords do not match.\n")
            return "register"

        display_name = inquirer.text(
            message="Display Name",
        ).execute()

        try:
            user = self.service.register(username, email, password, display_name)
            self.send_message(
                f"\n✔ Account created successfully! Welcome, {user.display_name}!\n"
            )
            user = self.service.login(username, password)
            self.on_success(user)  # hand the user up to the controller
            self.send_message(f"\nWelcome, {user.display_name}!\n")
            return "main_menu"

        except ValueError as e:
            self.send_message(f"\n✘ {e}\n")
            return "register"
