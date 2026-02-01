from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from features.user.service import UserService


class ProfileMenuScreen:
    """Menu for the currently logged-in user — no ID inputs needed."""

    def __init__(self, service: UserService, current_user):
        self.service = service
        self.current_user = current_user

    def render(self) -> str:
        print(
            f"\n  Logged in as: {self.current_user.display_name} (ID: {self.current_user.id})\n"
        )
        return inquirer.select(
            message="Profile",
            choices=[
                Choice("profile", name="View Profile"),
                Choice("change_display_name", name="Change Display Name"),
                Choice("delete_my_account", name="Delete My Account"),
                Choice("back", name="Back"),
            ],
        ).execute()


class ProfileScreen:
    """Displays the currently logged-in user's info."""

    def __init__(self, service: UserService, current_user):
        self.service = service
        self.current_user = current_user

    def render(self) -> str:
        try:
            # Re-fetch to always show the latest data
            user = self.service.get_user(self.current_user.id)
            print(f"\n  ID           : {user.id}")
            print(f"  Display Name : {user.display_name}")
            print(f"  Auth ID      : {user.auth_id}\n")
        except LookupError as e:
            print(f"\n✘ {e}\n")

        return "profile_menu"


class ChangeDisplayNameScreen:
    """Updates the display name of the currently logged-in user."""

    def __init__(self, service: UserService, current_user):
        self.service = service
        self.current_user = current_user

    def render(self) -> str:
        print(f"\n  Current display name: {self.current_user.display_name}\n")

        new_name = inquirer.text(
            message="Enter new display name",
        ).execute()

        try:
            updated = self.service.update_user(
                self.current_user.id, {"display_name": new_name}
            )
            self.current_user.display_name = updated.display_name  # sync session
            print(f"\n✔ Display name updated to: {updated.display_name}\n")
        except (ValueError, LookupError) as e:
            print(f"\n✘ Error: {e}\n")

        return "profile_menu"


class DeleteMyAccountScreen:
    """Deletes the currently logged-in user's account after confirmation."""

    def __init__(self, service: UserService, current_user):
        self.service = service
        self.current_user = current_user

    def render(self) -> str:
        print(
            f"\n  ⚠ This will permanently delete your account: {self.current_user.display_name}\n"
        )

        confirm = inquirer.confirm(
            message="Are you sure you want to delete your account?",
            default=False,
        ).execute()

        if not confirm:
            print("\n⚠ Deletion cancelled.\n")
            return "profile_menu"

        try:
            self.service.delete_user(self.current_user.id)
            print(f"\n✔ Account deleted successfully.\n")
            return "auth"  # account gone, force back to root
        except LookupError as e:
            print(f"\n✘ {e}\n")

        return "profile_menu"
