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
    def edit_phone(self, args):
        name, oldPhone, newPhone = args
        return self.addressBook.edit_phone(name, oldPhone, newPhone)

    @input_error
    def show_contact(self, args):
        name = args[0]
        search_result: Record = self.addressBook.find(name)
        return search_result

    def show_all_contacts(self):
        return str(self.addressBook)

    @input_error
    def add_birthday(self, args):
        name, birthday = args
        return self.addressBook.add_birthday(name, birthday)

    @input_error
    def edit_birthday(self, args):
        name, birthday = args
        return self.addressBook.edit_birthday(name, birthday)

    def birthdays(self):
        return self.addressBook.get_birthdays_per_week()

    @input_error
    def add_email(self, args):
        name, email = args
        return self.addressBook.add_email(name, email)

    @input_error
    def edit_email(self, args):
        name, email = args
        return self.addressBook.edit_email(name, email)

    @input_error
    def add_address(self, args):
        name, address = args
        return self.addressBook.add_address(name, address)

    @input_error
    def edit_address(self, args):
        name, address = args
        return self.addressBook.edit_address(name, address)

    @input_error
    def delete_contact(self, args):
        name, = args
        return self.addressBook.delete(name)

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
                elif command == "edit-phone":
                    print(self.edit_phone(args))
                elif command == "show-all-contacts":
                    print(self.show_all_contacts())
                elif command == "add-birthday":
                    print(self.add_birthday(args))
                elif command == "edit-birthday":
                    print(self.edit_birthday(args))
                elif command == "birthdays":
                    print(self.birthdays())
                elif command == "add-email":
                    print(self.add_email(args))
                elif command == "edit-email":
                    print(self.edit_email(args))
                elif command == "add-address":
                    print(self.add_address(args))
                elif command == "edit-address":
                    print(self.edit_address(args))
                elif command == "show-contact":
                    print(self.show_contact(args))
                elif command == "delete-contact":
                    print(self.delete_contact(args))
                else:
                    print("Invalid command.")
            except Exception:
                print("Invalid arguments for command:", command)
