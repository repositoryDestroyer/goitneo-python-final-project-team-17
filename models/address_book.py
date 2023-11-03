from datetime import datetime
from collections import defaultdict
from collections import UserDict

from .birthday import Birthday
from .name import Name
from .phone import Phone
from .record import Record


class AddressBook(UserDict):
    def add_record(self, record: Record):
        if not record:
            return

        record_name = record.get_name()
        self.data[record_name.value] = record

    def add_birthday(self, name, birthday):
        target_record: Record = self.find(name)
        if target_record:
            target_record.add_birthday(birthday)
            return "Birthday was added."
        raise IndexError

    def show_birthday(self, name):
        target_record: Record = self.find(name)
        if target_record:
            return target_record.show_birthday()
        raise KeyError

    def add_email(self, name, email):
        target_record: Record = self.find(name)
        if target_record:
            target_record.add_email(email)
            return "Email was added."
        raise KeyError

    def add_address(self, name, address):
        target_record: Record = self.find(name)
        if target_record:
            target_record.add_address(address)
            return "Address was added."
        raise KeyError

    def find(self, key):
        name = Name(key)
        res = self.data.get(name.value)
        return res

    def edit_record_phone(self, name, phone):
        target_record: Record = self.find(name)

        if target_record is None:
            return "Contact was not found."

        target_phone: Phone = target_record.find_phone(phone)

        # There is nothing to be updated (the phone is actual)
        if target_phone is not None:
            return "Contact updated."
        else:
            target_record.rewrite_phone(phone)

        return "Contact updated."

    def delete(self, key):
        del self.data[key]

    def get_birthdays(self, period):
        if int(period) < 1:
            return 'The number of days must be greater than 0.'
        today = datetime.today().date()
        prepared_data = defaultdict(list)
        birthday_result = ''

        for record in self.data.values():
            if not record.birthday:
                continue

            name = str(record.get_name())
            birthday = record.show_birthday().get_date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            delta_days = (birthday_this_year - today).days

            if delta_days > int(period):
                continue

            prepared_data[birthday_this_year].append(name)

        if len(prepared_data) == 0:
            birthday_result = f"There are no birthdays during next {period} days."
        else:
            birthday_result = "\n".join(
                [f"{day.strftime('%d.%m.%Y')}: {', '.join(names)}" for day, names in prepared_data.items()])

        return birthday_result

    def to_dict(self):
        data = {}
        for value in self.data.values():
            data.update({str(value.name): {"name": str(value.name),
                                           "phones": [str(phone) for phone in value.phones],
                                           "birthday": str(value.birthday)}})

        return data

    def from_dict(self, data):
        for name in data:
            raw_name = data[name]
            self.add_record(Record(Name(raw_name['name']),
                                   [Phone(p) for p in raw_name['phones']],
                                   None if raw_name['birthday'] == "None" else Birthday(raw_name['birthday'])))

    def __str__(self):
        prepared_data = []

        for value in self.data.values():
            prepared_data.append(str(value))

        return "\n".join(prepared_data)
