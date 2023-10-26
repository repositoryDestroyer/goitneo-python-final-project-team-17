from .name import Name
from .phone import Phone
from .birthday import Birthday
from exceptions.birthday_exists import BirthdayExists


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def get_name(self):
        return self.name

    def add_phone(self, phone_number):
        if phone_number:
            self.phones.append(Phone(phone_number))

    def add_birthday(self, birthday):
        if self.birthday:
            raise BirthdayExists
        self.birthday = Birthday(birthday)
        return "Birthday successfully added."

    def show_birthday(self):
        return self.birthday

    def rewrite_phone(self, new_number):
        if not new_number:
            return self.phones

        self.phones = [Phone(new_number)]

        return self.phones

    def edit_phone(self, number_to_edit, new_number):
        if not (number_to_edit or new_number):
            return self.phones

        for index, phone in enumerate(self.phones):
            if phone.value == number_to_edit:
                self.phones[index] = Phone(new_number)
                break

        return self.phones

    def find_phone(self, phone_number):
        if not phone_number:
            return None

        return next(
            filter(lambda number: number.value == phone_number, self.phones),
            None,
        )

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
