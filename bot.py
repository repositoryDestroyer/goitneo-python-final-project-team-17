import pickle
from decorators.input_error import input_error
from decorators.note_error import note_error
from exceptions.address_exists import AddressExists
from models.address_book import AddressBook
from models.note import Note, Notes, Tag
from models.record import Record
from utils.notes import dump_notes, load_notes
from utils.address_book import load_address_book, save_address_book


notes_json = "notes.json"
address_book_filename = "address_book.pickle"


class Bot:
    def __init__(self):
        self.address_book = load_address_book(address_book_filename)
        self.notes = Notes()
        self.notes.from_dict(load_notes(notes_json))

    def parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    @input_error
    def add_contact(self, args):
        name, phone = args

        prepared_record = Record(name)
        prepared_record.add_phone(phone)
        self.address_book.add_record(prepared_record)

        return "Contact added."

    @input_error
    def change_contact(self, args):
        name, phone = args

        return self.address_book.edit_record_phone(name, phone)

    @input_error
    def show_phone(self, args):
        name = args[0]

        search_result: Record = self.address_book.find(name)

        if search_result is None:
            return "Contact was not found."

        return search_result

    def show_all(self):
        return str(self.address_book)

    @input_error
    def add_birthday(self, args):
        name, birthday = args
        return self.address_book.add_birthday(name, birthday)

    @input_error
    def show_birthday(self, args):
        name = args[0]
        return self.address_book.show_birthday(name)

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

    @note_error
    def find_notes_by_word(self, args):
        word = args[0].strip().lower()

        return self.notes.find(word)

    @input_error
    def add_email(self, args):
        name, email = args
        return self.address_book.add_email(name, email)

    @input_error
    def add_address(self, args):
        name, address = args
        return self.address_book.add_address(name, address)

    def run(self):
        print("Welcome to the assistant bot!")

        while True:
            user_input = input("Enter a command: ")
            command, *args = self.parse_input(user_input)

            try:
                if command in ["close", "exit", "bye"]:
                    save_address_book(address_book_filename, self.address_book)
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
                    print(self.birthdays(args))
                elif command == "add-note":
                    print(self.create_note(args))
                elif command == "show-notes":
                    print(self.show_notes())
                elif command == "remove-note":
                    print(self.remove_note(args))
                elif command == "get-note":
                    print(self.get_note_by_title(args))
                elif command == "update-note":
                    print(self.update_note(args))
                elif command == "find-notes":
                    print(self.find_notes_by_word(args))
                elif command == "add-email":
                    print(self.add_email(args))
                elif command == "add-address":
                    print(self.add_address(args))
                else:
                    print("Invalid command.")
            except Exception as e:
                print("Error: ===> {}".format(e))
