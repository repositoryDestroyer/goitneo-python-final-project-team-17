from datetime import datetime
from collections import defaultdict
from collections import UserDict

from exceptions.missing_record import MissingRecord
from exceptions.record_exists import RecordExists

from .birthday import Birthday
from .name import Name
from .phone import Phone
from .record import Record


class AddressBook(UserDict):
    def add_record(self, record: Record):
        if not record:
            return

        record_name = record.get_name()

        if record_name.value in self.data:
            raise RecordExists
        self.data[record_name.value] = record

    def add_birthday(self, name, birthday):
        target_record: Record = self.find(name)
        target_record.add_birthday(birthday)
        return "Birthday was added."

    def edit_birthday(self, name, birthday):
        record: Record = self.find(name)
        record.edit_birthday(birthday)
        return "Birthday was edited"

    def add_email(self, name, email):
        target_record: Record = self.find(name)
        target_record.add_email(email)
        return "Email was added."

    def edit_email(self, name, email):
        target_record: Record = self.find(name)
        target_record.edit_email(email)
        return "Email edited."

    def add_address(self, name, address):
        target_record: Record = self.find(name)
        target_record.add_address(address)
        return "Address was added."

    def edit_address(self, name, address):
        target_record: Record = self.find(name)
        target_record.edit_address(address)

    def find(self, name):
        if name in self.data:
            return self.data[name]
        raise MissingRecord

    def edit_phone(self, name, old_phone, new_phone):
        record: Record = self.find(name)
        record.edit_phone(old_phone, new_phone)
        return "Phone was edited."

    def delete(self, name):
        self.find(name)  # To validate that it exists
        del self.data[name]
        return "Contact deleted."

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

    # def to_dict(self):
    #     data = {}
    #     for value in self.data.values():
    #         data.update({str(value.name): {"name": str(value.name),
    #                                        "phones": [str(phone) for phone in value.phones],
    #                                        "birthday": str(value.birthday)}})
    #     return data

    # def from_dict(self, data):
    #     for name in data:
    #         raw_name = data[name]
    #         self.add_record(Record(Name(raw_name['name']),
    #                                [Phone(p) for p in raw_name['phones']],
    #                                None if raw_name['birthday'] == "None" else Birthday(raw_name['birthday'])))

    def __str__(self):
        result = ""
        for value in self.data.values():
            result += str(value)
        return result
