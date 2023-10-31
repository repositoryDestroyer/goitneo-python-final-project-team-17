from decorators.input_error import input_error
from decorators.note_error import note_error
from models.address_book import AddressBook
from models.note import Note, Notes, Tag
from models.record import Record
from utils.contacts import dump_notes, load_notes


notes_json = 'notes.json'
contacts_json = 'contacts.json'


class Bot:
    def __init__(self):
        self.addressBook = AddressBook()
        self.notes = Notes()

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

    @note_error
    def create_note(self, args):
        title = args[0]

        text = input("Input Note text: ")
        raw_tags = input("Input tags like tag1,tag2,tag3... : ")

        tags = [Tag(tag.strip()) for tag in raw_tags.split(',')]
        note = Note(title=title, text=text, tags=tags)

        self.notes.add_note(note)
        dump_notes(notes_json, self.notes.to_dict())

        return "Note '{}' successfully added".format(note.title)

    def run(self):
        print("Welcome to the assistant bot!")

        while True:
            user_input = input("Enter a command: ")
            command, *args = self.parse_input(user_input)

            try:
                if command in ["close", "exit", "bye"]:
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
                elif command == "add-note":
                    print(self.create_note(args))
                elif command == "show-notes":
                    print(self.show_notes())
                elif command == "find-note":
                    print(self.find_note(args))
                elif command == "delete-note":
                    print(self.delete_note(args))
                elif command == "get-note":
                    print(self.get_note(args))
                elif command == "update-note":
                    print(self.update_note(args))
                else:
                    print("Invalid command.")
            except Exception:
                print("Invalid arguments for command:", command)

