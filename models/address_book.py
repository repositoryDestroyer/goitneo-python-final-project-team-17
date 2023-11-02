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
        raise KeyError

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

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        prepared_data = defaultdict(list)

        for record in self.data.values():
            if record.birthday != None:
                name = str(record.get_name())
                birthday = record.show_birthday().get_date()
                birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            delta_days = (birthday_this_year - today).days

            # skip if birhday is after week from today
            if delta_days >= 7:
                continue

            weekday = birthday_this_year.weekday()

            # check current weekday is weekend, move to the next monday
            if weekday in [5, 6]:
                prepared_data["Monday"] = (prepared_data["Monday"] or []) + [name]
            else:
                birthday = birthday_this_year.strftime("%A")
                prepared_data[birthday] = (prepared_data[birthday] or []) + [name]

        if len(prepared_data) == 0:
            print("There are no birthday colleagues during next week.")

        # simply print prepared birthday colleagues
        for day in prepared_data:
            birthday_colleagues = prepared_data[day]
            print(f"{day}: {', '.join(birthday_colleagues)}")

        # return prepared values just for unittest (plz, don't treat it as a wrong realization)
        return prepared_data

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
