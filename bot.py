from decorators.input_error import input_error
from decorators.note_error import note_error
from decorators.arguments_validator import arguments_validator
from decorators.search_phrase_validator import search_phrase_validator
from models.note import Note, Notes, Tag
from models.record import Record
from utils.notes import dump_notes, load_notes
from utils.address_book import load_address_book, save_address_book
from enums.command_enum import Command


notes_json = "notes.json"
address_book_filename = "address_book.pickle"


class Bot:
    def __init__(self, address_book=None):
        self.address_book = (
            address_book
            if address_book is not None
            else load_address_book(address_book_filename)
        )
        self.notes = Notes()
        self.notes.from_dict(load_notes(notes_json))
        self.allowed_commands = Command.list()

    def parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    @arguments_validator(["name", "phone"])
    @input_error
    def add_contact(self, args):
        name, phone = args

        prepared_record = Record(name)
        prepared_record.add_phone(phone)
        self.address_book.add_record(prepared_record)

        return "Contact added."

    @arguments_validator(["name", "phone"])
    @input_error
    def add_phone(self, args):
        name, phone = args
        self.address_book.add_phone(name, phone)

        return f"Phone to contact {name} added."

    @input_error
    def edit_phone(self, args):
        name, oldPhone, newPhone = args
        return self.address_book.edit_phone(name, oldPhone, newPhone)

    @arguments_validator(["name"])
    @input_error
    def show_contact(self, args):
        name = args[0]
        search_result: Record = self.address_book.find(name)
        return search_result

    def show_all_contacts(self):
        return str(self.address_book)

    @arguments_validator(["name", "birthday"])
    @input_error
    def add_birthday(self, args):
        name, birthday = args
        return self.address_book.add_birthday(name, birthday)

    @arguments_validator(["name", "birthday"])
    @input_error
    def edit_birthday(self, args):
        name, birthday = args
        return self.address_book.edit_birthday(name, birthday)

    def birthdays(self, args):
        period = args[0]
        return self.address_book.get_birthdays(period)

    @note_error
    def create_note(self, args):
        title = args[0]

        text = input("Input Note text: ")
        raw_tags = input("Input tags like tag1,tag2,tag3... : ")

        tags = []
        for tag in raw_tags.split(","):
            if tag:
                tags.append(Tag(tag.strip()))

        note = Note(title=title, text=text, tags=tags)

        response = self.notes.add_note(note)
        dump_notes(notes_json, self.notes.to_dict())

        return response

    @note_error
    def show_notes(self):
        return self.notes.get_all_notes()

    @note_error
    def remove_note(self, args):
        try:
            note = self.notes.delete_note(args[0])
        except IndexError:
            return "There is no the note."

        dump_notes(notes_json, self.notes.to_dict())
        return note

    @note_error
    def get_note_by_title(self, args):
        note = args[0].strip().lower()

        result = []
        for key, value in self.notes.items():
            if note == key:
                result = "title: {}, text: {}, tags: {}".format(
                    value.title, value.text, value.tags
                )
                return result
        return "There are no results with {}".format(note)

    @note_error
    def update_note(self, args):
        note: Note = None

        try:
            if args[0]:
                title = " ".join(args).lower()
        except IndexError as e:
            return "{}".format(e)

        for key, value in self.notes.items():
            if title == key.lower():
                note = value

        if note == None:
            return "No Note."

        change_request = input(
            "Press 1 for title changing, Press 2 for text changing, Press 3 for tag changing: "
        )

        match change_request:
            case "1":
                old_title = note.title
                new_title = input("Input new title: ")

                if new_title == "":
                    raise IndexError("Incorrect title input.")

                note.update_title(new_title)
                self.notes.pop(old_title)
                self.notes[new_title] = note
                dump_notes(notes_json, self.notes.to_dict())

                return "{} has been changed to {}".format(old_title, new_title)

            case "2":
                old_text = note.text
                new_text = input("Input new text: ")

                note.update_text(new_text)
                self.notes[note.title] = note
                dump_notes(notes_json, self.notes.to_dict())

                return "{} has been changed to {}".format(old_text, new_text)

            case "3":
                old_tags = note.tags
                raw_new_tags = input("Input new tag: ")

                new_tags = [Tag(tag.strip())
                            for tag in raw_new_tags.split(",")]
                note.update_tags(new_tags)
                self.notes[note.title] = note
                dump_notes(notes_json, self.notes.to_dict())

                return "{} has been changed to {}".format(old_tags, new_tags)

            case _:
                raise IndexError("Incorrect input.") from None

    @search_phrase_validator
    @input_error
    def find_contacts_by_name(self, args):
        search_phrase = args[0].strip()
        return self.address_book.find_by_name(search_phrase)

    @search_phrase_validator
    @input_error
    def find_contacts_by_phone(self, args):
        search_phrase = args[0].strip()
        return self.address_book.find_by_phone(search_phrase)

    @search_phrase_validator
    @input_error
    def find_contacts_by_email(self, args):
        search_phrase = args[0].strip()
        return self.address_book.find_by_email(search_phrase)

    @search_phrase_validator
    @input_error
    def find_contacts_by_address(self, args):
        search_phrase = args[0].strip()
        return self.address_book.find_by_address(search_phrase)

    @arguments_validator(["word"])
    @note_error
    def find_notes_by_word(self, args):
        word = args[0].strip().lower()

        return self.notes.find(word)

    @arguments_validator(["name", "email"])
    @input_error
    def add_email(self, args):
        name, email = args
        return self.address_book.add_email(name, email)

    @arguments_validator(["name", "email"])
    @input_error
    def edit_email(self, args):
        name, email = args
        return self.address_book.edit_email(name, email)

    @arguments_validator(["name", "address"])
    @input_error
    def add_address(self, args):
        name, address = args
        return self.address_book.add_address(name, address)

    @arguments_validator(["name", "address"])
    @input_error
    def edit_address(self, args):
        name, address = args
        return self.address_book.edit_address(name, address)

    @arguments_validator(["name"])
    @input_error
    def delete_contact(self, args):
        (name,) = args
        return self.address_book.delete(name)

    def __handle_invalid_command(self, command):
        partial_match = command
        matching_records = [
            command for command in self.allowed_commands if partial_match in command
        ]

        if len(matching_records):
            commands_list = '\n'.join(matching_records)
            print(
                f"Maybe you wanted to choose some of these commands:\n{commands_list}"
            )
            return

        print("Invalid command.")

    def show_all_commands(self):
        return '\n'.join(self.allowed_commands)

    def run(self):
        print("Welcome to the assistant bot!")

        while True:
            user_input = input("Enter a command: ")
            command, *args = self.parse_input(user_input)

            try:
                if command in [
                    Command.CLOSE.value,
                    Command.EXIT.value,
                    Command.BYE.value,
                ]:
                    save_address_book(address_book_filename, self.address_book)
                    print("Good bye!")
                    break
                elif command == Command.HELLO.value:
                    print("How can I help you?")
                elif command == Command.HELP.value:
                    print(self.show_all_commands())
                elif command == Command.ADD.value:
                    print(self.add_contact(args))
                elif command == Command.ADD_PHONE.value:
                    print(self.add_phone(args))
                elif command == Command.EDIT_PHONE.value:
                    print(self.edit_phone(args))
                elif command == Command.ADD_EMAIL.value:
                    print(self.add_email(args))
                elif command == Command.EDIT_EMAIL.value:
                    print(self.edit_email(args))
                elif command == Command.ADD_ADDRESS.value:
                    print(self.add_address(args))
                elif command == Command.EDIT_ADDRESS.value:
                    print(self.edit_address(args))
                elif command == Command.ADD_BIRTHDAY.value:
                    print(self.add_birthday(args))
                elif command == Command.EDIT_BIRTHDAY.value:
                    print(self.edit_birthday(args))
                elif command == Command.SHOW_CONTACT.value:
                    print(self.show_contact(args))
                elif command == Command.SHOW_CONTACTS.value:
                    print(self.show_all_contacts())
                elif command == Command.DELETE_CONTACT.value:
                    print(self.delete_contact(args))
                elif command == Command.BIRTHDAYS.value:
                    print(self.birthdays(args))
                elif command == Command.ADD_NOTE.value:
                    print(self.create_note(args))
                elif command == Command.SHOW_NOTES.value:
                    print(self.show_notes())
                elif command == Command.REMOVE_NOTE.value:
                    print(self.remove_note(args))
                elif command == Command.GET_NOTE.value:
                    print(self.get_note_by_title(args))
                elif command == Command.UPDATE_NOTE.value:
                    print(self.update_note(args))
                elif command == Command.FIND_NOTES.value:
                    print(self.find_notes_by_word(args))
                elif command == Command.FIND_CONTACTS_BY_NAME.value:
                    print(self.find_contacts_by_name(args))
                elif command == Command.FIND_CONTACTS_BY_PHONE.value:
                    print(self.find_contacts_by_phone(args))
                elif command == Command.FIND_CONTACTS_BY_EMAIL.value:
                    print(self.find_contacts_by_email(args))
                elif command == Command.FIND_CONTACTS_BY_ADDRESS.value:
                    print(self.find_contacts_by_address(args))
                else:
                    self.__handle_invalid_command(command)
            except Exception as e:
                print("Error: ===> {}".format(e))
