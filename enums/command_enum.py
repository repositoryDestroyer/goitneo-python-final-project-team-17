from enum import Enum


class Command(Enum):
    HELLO = "hello"
    HELP = "help"
    ADD = "add"
    ADD_BIRTHDAY = "add-birthday"
    EDIT_BIRTHDAY = "edit-birthday"
    BIRTHDAYS = "birthdays"
    ADD_EMAIL = "add-email"
    EDIT_EMAIL = "edit-email"
    ADD_ADDRESS = "add-address"
    EDIT_ADDRESS = "edit-address"
    ADD_PHONE = "add-phone"
    EDIT_PHONE = "edit-phone"
    SHOW_CONTACTS = "show-contacts"
    SHOW_CONTACT = "show-contact"
    DELETE_CONTACT = "delete-contact"
    ADD_NOTE = "add-note"
    SHOW_NOTES = "show-notes"
    REMOVE_NOTE = "remove-note"
    GET_NOTE = "get-note"
    UPDATE_NOTE = "update-note"
    FIND_NOTES = "find-notes"
    FIND_CONTACTS_BY_NAME = "find-contacts-by-name"
    FIND_CONTACTS_BY_PHONE = "find-contacts-by-phone"
    FIND_CONTACTS_BY_EMAIL = "find-contacts-by-email"
    FIND_CONTACTS_BY_ADDRESS = "find-contacts-by-address"
    CLOSE = "close"
    EXIT = "exit"
    BYE = "bye"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
