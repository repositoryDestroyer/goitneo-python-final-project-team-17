import re
from exceptions.wrong_email_format import WrongEmailFormat
from models.field import Field


class Email(Field):
    def __init__(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+(\.\w+)+$"
        if not re.match(pattern, email):
            raise WrongEmailFormat("Invalid email format")
        super().__init__(email)
