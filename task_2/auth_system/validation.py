from email_validator import validate_email, EmailNotValidError
import re

class ValidationError(Exception):
    def __init__(self, message, *args):
        self.message = message
        super().__init__(*args)
        
def is_email_valid(email, auth_system): 
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        raise ValidationError(str(e))

def is_email_unique(email: str, auth_system): 
    email = email.lower()
    for user in auth_system.all_users:
        if user.email.lower() == email:
            raise ValidationError("This email already exists!")

def is_username_valid(username, auth_system):
    if len(username) < 8:
        raise ValidationError("Username should be at least 8 characters!")
    
    if re.search(r"^[\w]*$", username) is None:
        raise ValidationError("Username can only contains alphanumeric characters and underscore!")
    
def is_username_unique(username, auth_system):
    for user in auth_system.all_users:
        if user.username == username:
            raise ValidationError("This username already exists!")

def is_password_valid(password, auth_system):
    if len(password) < 6:
        raise ValidationError("Password should be at least 6!")

DEFAULT_VALIDATORS = {
    "username": [is_username_valid, is_username_unique],
    "email": [is_email_valid, is_email_unique],
    "password": [is_password_valid],
}

