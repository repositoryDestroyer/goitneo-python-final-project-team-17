from datetime import datetime
from .field import Field
from exceptions.wrong_birthday_format import WrongBirthdayFormat


class Birthday(Field):
    def __init__(self, birthday):
        self.__date_format = "%d.%m.%Y"

        try:
            value = datetime.strptime(birthday, self.__date_format)
        except ValueError:
            raise WrongBirthdayFormat
        super().__init__(value)

    def get_date(self):
        return self.value.date()

    def __str__(self):
        return f"{self.value.strftime(self.__date_format)}"
