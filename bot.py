from decorators.input_error import input_error
from decorators.note_error import note_error
from models.address_book import AddressBook
from models.note import Note, Notes, Tag
from models.record import Record
from utils.contacts import dump_notes, load_notes


notes_json = 'notes.json'


class Bot:

    def __init__(self):
        self.addressBook = AddressBook()
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
        notes: Notes = self.notes

        text = input("Input Note text: ")
        raw_tags = input("Input tags like tag1,tag2,tag3... : ")

        tags = [Tag(tag.strip()) for tag in raw_tags.split(',')]
        note = Note(title=title, text=text, tags=tags)

        notes.add_note(note)
        dump_notes(notes_json, notes.to_dict())

        return "Note {} successfully added".format(note.title)

    @note_error
    def show_notes(self):
        return self.notes.get_all_notes()

    @note_error
    def remove_note(self, args):
        try:
            word, notes = self.notes.delete_note(args[0])
        except IndexError:
            return 'There is no the note.'

        dump_notes(notes_json, notes.to_dict())
        return 'Note {} has been deleted.'.format(word.capitalize())

    @note_error
    def get_note(self, args):
        note = args[0].strip().lower()

        result = []
        for key, value in self.notes.items():
            if note in "{} {} {}".format(str(value.title).lower(),
                                         str(value.text).lower(),
                                         str(' '.join([str(tag) for tag in value.tags])).lower()):
                result = ('{} : {}, {}, {}'.format(key, value.title, value.text, value.tags))
                return result
        return 'There are no results with {}'.format(note)

    @note_error
    def update_note(self, args):
        note: Note = None

        try:
            if args[0]:
                title = ' '.join(args).lower()
        except IndexError:
            raise IndexError('Incorrect title input.') from None

        for key, value in self.notes.items():
            if title == key.lower():
                note = value

        if note == None:
            return "No Note.", self.notes

        change_request = input("Press 1 for title changing, Press 2 for text changing, Press 3 for tag changing: ")

        match change_request:
            case '1':
                old_title = note.title
                new_title = input('Input new title: ')

                if new_title == '':
                    raise IndexError("Incorrect title input.")

                note.update_title(new_title)
                self.notes.pop(old_title)
                self.notes[new_title] = note
                dump_notes(notes_json, self.notes.to_dict())

                return '{} has been changed to {}'.format(old_title, new_title)

            case '2':
                old_text = note.text
                new_text = input('Input new text: ')

                note.update_text(new_text)
                self.notes[note.title] = note
                dump_notes(notes_json, self.notes.to_dict())

                return '{} has been changed to {}'.format(old_text, new_text)

            case '3':
                old_tags = note.tags
                raw_new_tags = input('Input new tag: ')

                new_tags = [Tag(tag.strip()) for tag in raw_new_tags.split(',')]
                note.update_tags(new_tags)
                self.notes[note.title] = note
                dump_notes(notes_json, self.notes.to_dict())

                return '{} has been changed to {}'.format(old_tags, new_tags)

            case _:
                raise IndexError('Введіть коррекно дані') from None

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
                elif command == "remove-note":
                    print(self.remove_note(args))
                elif command == "get-note":
                    print(self.get_note(args))
                elif command == "update-note":
                    print(self.update_note(args))
                else:
                    print("Invalid command.")
            except Exception as e:
                print('Error: ===> {}'.format(e))

