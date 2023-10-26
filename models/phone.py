from .field import Field

from exceptions.wrong_phone_format import WrongPhoneFormat
import re


class Phone(Field):
    def __init__(self, phone):
        pattern = r"^\d{10}$"

        if not re.match(pattern, phone):
            raise WrongPhoneFormat("Phone should consist of 10 digits")
        super().__init__(phone)
