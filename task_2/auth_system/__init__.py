from typing import Callable, Optional
from .validation import DEFAULT_VALIDATORS
from .user import User
import os
import json
import argon2


class AuthSystem:
    def __init__(
        self,
        dir_path=None,
        default_validators: Optional[dict[str, Callable]] = DEFAULT_VALIDATORS,
    ):
        self.default_validators = default_validators
        
        if dir_path is not None:
            self.json_path = os.path.join(dir_path, "users.json")
        else:
            self.json_path = "users.json"
        self._init_json_file()
        
        self._password_hasher = argon2.PasswordHasher()

    def register(
        self,
        user: User,
        # extra_validators: Optional[dict[str, list[Callable]]] = {},
    ):
        """This function validates provided data using self.default_validators and creates a new user.

        throws an exception of type ValidationError if data is not valid
        or any other suitable exception type in case of unexpected errors.
        """

        # run default validators
        for field, validators_list in self.default_validators.items():
            for validator in validators_list:
                validator(getattr(user, field), self)

        # # run extra validators
        # for field, validators_list in extra_validators.items():
        #     for validator in validators_list:
        #         validator(getattr(user, field), self)

        hashed_password = self._password_hasher.hash(user.password)

        # add new user
        with open(self.json_path, "r") as f:
            all_users_raw = json.load(f)
        all_users_raw.append(
            {
                "username": user.username,
                "email": user.email,
                "password": hashed_password,
            }
        )
        with open(self.json_path, "w") as f:
            json.dump(all_users_raw, f)

        # Invalidate the old cache
        self._all_users = None

    def login(self, username_or_email, password):
        """It tries to login a user returning a user object (without password) on success or None otherwise"""
        with open(self.json_path, "r") as f:
            all_users_raw = json.load(f)

        for user_dict in all_users_raw:
            if (
                username_or_email == user_dict["username"]
                or username_or_email == user_dict["email"]
            ):
                try:
                    self._password_hasher.verify(user_dict['password'], password)
                except Exception:
                    return None
                else:
                    return User(user_dict["username"], user_dict["email"], None)
        return None
    
    @property
    def all_users(self):
        """Returns a list of all the users (without password) in the system"""
        if not hasattr(self, "_all_users") or self._all_users is None:
            with open(self.json_path, "r") as f:
                self._all_users = [
                    User(dict["username"], dict["email"], None) for dict in json.load(f)
                ]

        return self._all_users
    
    def _init_json_file(self):
        if not os.path.exists(self.json_path):
            with open(self.json_path, "w") as f:
                json.dump([], f)
        self.json_path


if __name__ == "__main__":
    AuthSystem()
