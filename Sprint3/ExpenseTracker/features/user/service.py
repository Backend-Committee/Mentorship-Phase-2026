from features.user.IUserRepo import IUserRepo
from features.user.model import User


class UserService:
    def __init__(self, user_repo: IUserRepo):
        self.user_repo = user_repo

    def create_user(self, display_name: str, auth_id: int) -> User:
        if not display_name or not display_name.strip():
            raise ValueError("Display name cannot be empty.")
        return self.user_repo.create_user(display_name.strip(), auth_id)

    def get_user(self, id: int) -> User:
        user = self.user_repo.get_user(id)
        if user is None:
            raise LookupError(f"User with id {id} not found.")
        return user

    def update_user(self, id: int, data: dict) -> User:
        # Ensure user exists before attempting update
        self.get_user(id)

        if "display_name" in data:
            if not data["display_name"] or not data["display_name"].strip():
                raise ValueError("Display name cannot be empty.")
            data["display_name"] = data["display_name"].strip()

        updated = self.user_repo.update_user(id, data)
        if updated is None:
            raise LookupError(f"User with id {id} not found.")
        return updated

    def delete_user(self, id: int) -> None:
        # Ensure user exists before attempting delete
        self.get_user(id)

        deleted = self.user_repo.delete_user(id)
        if not deleted:
            raise LookupError(f"User with id {id} not found.")
