import hashlib
import re

from features.auth.IAuthInfoRepo import IAuthInfoRepo
from features.auth.model import AuthInfo
from features.user.IUserRepo import IUserRepo
from features.user.model import User


class AuthService:
    def __init__(self, auth_repo: IAuthInfoRepo, user_repo: IUserRepo):
        self.auth_repo = auth_repo
        self.user_repo = user_repo

    # ─── Hashing ─────────────────────────────────────────────────

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def _verify_password(password: str, hashed: str) -> bool:
        return hashlib.sha256(password.encode()).hexdigest() == hashed

    # ─── Validation ──────────────────────────────────────────────

    @staticmethod
    def _validate_email(email: str) -> bool:
        return bool(
            re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
        )

    # ─── Register ────────────────────────────────────────────────

    def register(
        self, username: str, email: str, password: str, display_name: str
    ) -> User:
        """Create auth credentials + user profile atomically."""

        # Validations
        if not username or not username.strip():
            raise ValueError("Username cannot be empty.")
        if not email or not email.strip():
            raise ValueError("Email cannot be empty.")
        if not self._validate_email(email.strip()):
            raise ValueError("Invalid email format.")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")
        if not display_name or not display_name.strip():
            raise ValueError("Display name cannot be empty.")

        # Duplicate checks
        if self.auth_repo.get_by_username(username.strip()):
            raise ValueError("Username is already taken.")
        if self.auth_repo.get_by_email(email.strip()):
            raise ValueError("Email is already registered.")

        # Create AuthInfo first, then User with the new auth_id
        hashed = self._hash_password(password)
        auth_info = self.auth_repo.create(username.strip(), email.strip(), hashed)
        user = self.user_repo.create_user(display_name.strip(), auth_info.id)

        return user

    # ─── Login ───────────────────────────────────────────────────

    def login(self, username: str, password: str) -> User:
        """Verify credentials and return the linked User profile."""

        auth_info = self.auth_repo.get_by_username(username.strip() if username else "")
        if auth_info is None:
            raise ValueError("Invalid username or password.")

        if not self._verify_password(password, auth_info.hashed_password):
            raise ValueError("Invalid username or password.")

        # Fetch the linked User profile
        user = self.user_repo.get_user_by_auth_id(auth_info.id)
        if user is None:
            raise LookupError("User profile not found for this account.")

        return user
