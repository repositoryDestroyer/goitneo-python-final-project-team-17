from enum import Enum


class Command(Enum):
    HELLO = "hello"
    ADD = "add"
    CHANGE = "change"
    PHONE = "phone"
    ALL = "all"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    BIRTHDAYS = "birthdays"
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
    ADD_EMAIL = "add-email"
    ADD_ADDRESS = "add-address"
    EDIT_EMAIL = "edit-email"
    DELETE_CONTACT = "delete-contact"
    SHOW_CONTACTS = "show-contacts"
    SHOW_CONTACT = "show-contact"
    EDIT_BIRTHDAY = "edit-birthday"
    EDIT_ADDRESS = "edit-address"
    EDIT_PHONE = "edit-phone"
    ADD_PHONE = "add-phone"
    CLOSE = "close"
    EXIT = "exit"
    BYE = "bye"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
