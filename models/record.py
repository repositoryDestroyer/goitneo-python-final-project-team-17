from exceptions.address_exists import AddressExists
from exceptions.email_exists import EmailExists
from exceptions.phone_exists import PhoneExists
from .address import Address
from .email import Email
from .name import Name
from .phone import Phone
from .birthday import Birthday
from exceptions.birthday_exists import BirthdayExists


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def get_name(self):
        return self.name

    def add_phone(self, phone_number):
        if phone_number:
            phone = Phone(phone_number)

            for exist_phone in self.phones:
                if phone.value == exist_phone.value:
                    raise PhoneExists
            self.phones.append(phone)

    def add_birthday(self, birthday):
        if self.birthday:
            raise BirthdayExists
        self.birthday = Birthday(birthday)

    def edit_birthday(self, birthday):
        self.birthday = birthday

    def show_birthday(self):
        return self.birthday

    def add_email(self, email):
        if self.email:
            raise EmailExists
        self.email = Email(email)

        return "Email successfully added."

    def edit_email(self, email):
        self.email = Email(email)

        return "Email successfully added."

    def add_address(self, address):
        if self.address:
            raise AddressExists
        self.address = Address(address)
        return "Address successfully added."

    def edit_address(self, address):
        self.address = address

    def rewrite_phone(self, new_number):
        if not new_number:
            return self.phones

        self.phones = [Phone(new_number)]

        return self.phones

    def edit_phone(self, number_to_edit, new_number):
        if not (number_to_edit or new_number):
            return self.phones

        for exist_phone in self.phones:
            if new_number == exist_phone.value:
                raise PhoneExists

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
        return f"""
Contact name: {self.name.value}
phones: {'; '.join(p.value for p in self.phones)}
email: {self.email}
birthday: {self.birthday}
address: {self.address}
"""
