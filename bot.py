from decorators.input_error import input_error
from exceptions.address_exists import AddressExists
from models.address_book import AddressBook
from models.record import Record


class Bot:
    def __init__(self):
        self.addressBook = AddressBook()

    def parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    @input_error
    def add_contact(self, args):
        name, phone = args

        prepared_record = Record(name)
        prepared_record.add_phone(phone)
        self.addressBook.add_record(prepared_record)

        return "Contact added."

    @input_error
    def change_contact(self, args):
        name, phone = args

        return self.addressBook.edit_record_phone(name, phone)

    @input_error
    def show_phone(self, args):
        name = args[0]

        search_result: Record = self.addressBook.find(name)

        if search_result is None:
            return "Contact was not found."

        return search_result

    def show_all(self):
        return str(self.addressBook)

    @input_error
    def add_birthday(self, args):
        name, birthday = args
        return self.addressBook.add_birthday(name, birthday)

    @input_error
    def show_birthday(self, args):
        name = args[0]
        return self.addressBook.show_birthday(name)

    def birthdays(self):
        return self.addressBook.get_birthdays_per_week()

    @input_error
    def add_email(self, args):
        name, email = args
        return self.addressBook.add_email(name, email)

    @input_error
    def add_address(self, args):
        name, address = args
        return self.addressBook.add_address(name, address)

    def run(self):
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = self.parse_input(user_input)

            try:
                if command in ["close", "exit"]:
                    print("Good bye!")
                    break
                elif command == "hello":
                    print("How can I help you?")
                elif command == "add":
                    print(self.add_contact(args))
                elif command == "change":
                    print(self.change_contact(args))
                elif command == "phone":
                    print(self.show_phone(args))
                elif command == "all":
                    print(self.show_all())
                elif command == "add-birthday":
                    print(self.add_birthday(args))
                elif command == "show-birthday":
                    print(self.show_birthday(args))
                elif command == "birthdays":
                    print(self.birthdays())
                elif command == "add-email":
                    print(self.add_email(args))
                elif command == "add-address":
                    print(self.add_address(args))
                else:
                    print("Invalid command.")
            except Exception:
                print("Invalid arguments for command:", command)
