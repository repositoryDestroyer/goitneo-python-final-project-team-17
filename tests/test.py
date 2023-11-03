from re import S
import unittest

from models.address_book import *
from bot import Bot


class Test(unittest.TestCase):
    def test_record_add_phone_happy_flow(self):
        john_record = Record("John")
        john_record.add_phone("1234567890")

        self.assertEqual(john_record.phones[0].value, "1234567890")

    def test_record_add_phone_empty_phone(self):
        john_record = Record("John")
        john_record.add_phone("")

        self.assertEqual(len(john_record.phones), 0)

    def test_record_edit_phone_happy_flow(self):
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.edit_phone("1234567890", "0987654321")

        self.assertEqual(john_record.phones[0].value, "0987654321")

    def test_record_edit_phone_empty_args(self):
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.edit_phone("", "")

        self.assertEqual(john_record.phones[0].value, "1234567890")

    def test_record_find_phone(self):
        john_record = Record("John")
        john_record.add_phone("1234567890")
        happy_flow_search = john_record.find_phone("1234567890")
        wrong_phone_search = john_record.find_phone("")

        self.assertEqual(happy_flow_search.value, "1234567890")
        self.assertEqual(wrong_phone_search, None)

    def test_address_book_add_record(self):
        record_name = "John"
        book = AddressBook()
        john_record = Record(record_name)

        john_record.add_phone("1234567890")
        book.add_record(john_record)
        book.add_record({})

        self.assertEqual(
            len(book.data.values()),
            1,
        )
        self.assertEqual(
            book.data.get(record_name).get_name().value,
            record_name,
        )

    def test_address_book_find_record(self):
        record_name = "Vasyl"
        book = AddressBook()
        vasyl_record = Record(record_name)

        vasyl_record.add_phone("1234567890")
        book.add_record(vasyl_record)

        search_result = book.find(record_name)
        self.assertEqual(
            len(book.data.values()),
            1,
        )
        self.assertEqual(
            search_result.get_name().value,
            record_name,
        )

    def test_address_book_delete_record(self):
        vasyl_record_name = "Vasyl"
        ivan_record_name = "Ivan"
        book = AddressBook()
        vasyl_record = Record(vasyl_record_name)
        ivan_record = Record(ivan_record_name)

        vasyl_record.add_phone("1234567890")
        book.add_record(vasyl_record)
        book.add_record(ivan_record)
        book.delete(vasyl_record_name)

        search_result = book.find(ivan_record_name)
        self.assertEqual(
            len(book.data.values()),
            1,
        )
        self.assertEqual(
            search_result.get_name().value,
            ivan_record_name,
        )

    def test_add_contact_happy_flow(self):
        bot = Bot(address_book=AddressBook())
        result = bot.add_contact(["John", "8572156295"])
        record: Record = bot.address_book.find("John")

        self.assertEqual(record.phones[0].value, "8572156295")
        self.assertEqual(result, "Contact added.")

    def test_add_contact_wrong_args(self):
        bot = Bot(address_book=AddressBook())
        result = bot.add_contact([])

        self.assertEqual(len(bot.address_book) == 0, True)
        self.assertEqual(result, "Give me next arguments, please: name, phone")

    def test_edit_phone_happy_flow(self):
        bot = Bot()
        bot.add_contact(["John", "1234569012"])

        result = bot.edit_phone(["John", "9999999999"])
        record: Record = bot.address_book.find("John")
        result = bot.edit_phone(["John", "1234569012", "9999999999"])
        record: Record = bot.address_book.find("John")

        self.assertEqual(record.phones[0].value, "9999999999")
        self.assertEqual(result, "Phone was edited.")

    def test_edit_phone_not_found(self):
        bot = Bot()
        bot.add_contact(["Joshua", "1234569012"])
        result = bot.edit_phone([])
        record: Record = bot.address_book.find("Joshua")

        self.assertEqual(record.phones[0].value, "1234569012")
        self.assertEqual(result, "Give me name and phone please.")

    def test_edit_phone_wrong_args(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Johan", "1234511111"])
        result = bot.edit_phone(["Jack", "9999999991", "9999999999"])

        self.assertEqual(result, "Contact was not found. Add contact first.")

    def test_show_phone_happy_flow(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1114511111"])
        result = bot.show_contact(["Joshua"])

        self.assertEqual(
            str(result),
            "\nContact name: Joshua\nphones: 1114511111\nemail: None\nbirthday: None\naddress: None\n",
        )

    def test_show_phone_not_found(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1114511111"])
        result = bot.show_contact(["Vasyl"])

        self.assertEqual(result, "Contact was not found. Add contact first.")

    def test_show_phone_wrond_args(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        result = bot.show_contact([])
        record: Record = bot.address_book.find("Joshua")

        self.assertEqual(record.phones[0].value, "1110011111")
        self.assertEqual(result, "Give me next argument, please: name")

    def test_show_all(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        bot.add_contact(["Steve", "2928274219"])
        result = bot.show_all_contacts()

        self.assertEqual(
            str(result),
            "\nContact name: Joshua\nphones: 1110011111\nemail: None\nbirthday: None\naddress: None\n\nContact name: Steve\nphones: 2928274219\nemail: None\nbirthday: None\naddress: None\n",
        )

    def test_add_email(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        result = bot.add_email(["Joshua", "joshua@gmail.com"])

        record: Record = bot.address_book.find("Joshua")
        self.assertEqual(str(record.email), "joshua@gmail.com")
        self.assertEqual(str(result), "Email was added.")

    def test_add_email_twice(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        first_added = bot.add_email(["Joshua", "joshua@gmail.com"])
        second_added = bot.add_email(["Joshua", "joshua@gmail.com"])

        self.assertEqual(first_added, "Email was added.")
        self.assertEqual(second_added, "Email exists")

    def test_add_email_invalid_format(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        result = bot.add_email(["Joshua", "invalid_email"])

        self.assertEqual(result, "Invalid email format")

    def test_add_address(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        result = bot.add_address(["Joshua", "Street 1 Some town"])

        record: Record = bot.address_book.find("Joshua")
        self.assertEqual(
            str(record.address),
            "Street 1 Some town",
        )
        self.assertEqual(
            str(result),
            "Address was added.",
        )

    def test_find_contacts_by_name_happy_flow(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        result = bot.find_contacts_by_name(["hua"])

        self.assertEqual(
            result,
            "\nContact name: Joshua\nphones: 1110011111\nemail: None\nbirthday: None\naddress: None\n",
        )

    def test_find_contacts_by_name_error(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        result = bot.find_contacts_by_name(["h"])

        self.assertEqual(
            result,
            "Search phrase is too short. It should contain at least 2 chars.",
        )

    def test_find_contacts_by_name_no_results(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        result = bot.find_contacts_by_name(["tor"])

        self.assertEqual(
            result,
            "No records were found by search_phrase: tor",
        )

    def test_find_contacts_by_phone_happy_flow(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        result = bot.find_contacts_by_phone(["00"])

        self.assertEqual(
            result,
            "\nContact name: Joshua\nphones: 1110011111\nemail: None\nbirthday: None\naddress: None\n",
        )

    def test_find_contacts_by_phone_error(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        result = bot.find_contacts_by_phone(["9"])

        self.assertEqual(
            result,
            "Search phrase is too short. It should contain at least 2 chars.",
        )

    def test_find_contacts_by_phone_no_results(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        result = bot.find_contacts_by_phone(["999"])

        self.assertEqual(
            result,
            "No records were found by search_phrase: 999",
        )

    def test_find_contacts_by_email_happy_flow(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        bot.add_email(["Joshua", "test@gmail.com"])
        result = bot.find_contacts_by_email(["est@"])

        self.assertEqual(
            result,
            "\nContact name: Joshua\nphones: 1110011111\nemail: test@gmail.com\nbirthday: None\naddress: None\n",
        )

    def test_find_contacts_by_email_error(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        bot.add_email(["Joshua", "test2@gmail.com"])
        result = bot.find_contacts_by_email(["t"])

        self.assertEqual(
            result,
            "Search phrase is too short. It should contain at least 2 chars.",
        )

    def test_find_contacts_by_email_no_results(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        bot.add_email(["Joshua", "test3@gmail.com"])
        result = bot.find_contacts_by_email(["joshua@gmail"])

        self.assertEqual(
            result,
            "No records were found by search_phrase: joshua@gmail",
        )

    def test_find_contacts_by_address_happy_flow(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        bot.add_address(["Joshua", "Kluuvikatu 36"])
        result = bot.find_contacts_by_address(["ikat"])

        self.assertEqual(
            result,
            "\nContact name: Joshua\nphones: 1110011111\nemail: None\nbirthday: None\naddress: Kluuvikatu 36\n",
        )

    def test_find_contacts_by_address_error(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        bot.add_address(["Joshua", "Kluuvikatu 36"])
        result = bot.find_contacts_by_address(["u"])

        self.assertEqual(
            result,
            "Search phrase is too short. It should contain at least 2 chars.",
        )

    def test_find_contacts_by_address_no_results(self):
        bot = Bot(address_book=AddressBook())
        bot.add_contact(["Joshua", "1110011111"])
        bot.add_address(["Joshua", "Kluuvikatu 36"])
        result = bot.find_contacts_by_address(["kukva 36"])

        self.assertEqual(
            result,
            "No records were found by search_phrase: kukva 36",
        )

    def test_edit_email(self):
        bot = Bot()
        bot.add_contact(["Joshua", "1110011111"])
        bot.add_email(["Joshua", "Joshua@gmail.com"])
        result = bot.edit_email(["Joshua", "Joshua@hotmail.com"])

        record: Record = bot.address_book.find("Joshua")
        self.assertEqual(
            str(record.email),
            "Joshua@hotmail.com",
        )
        self.assertEqual(
            str(result),
            "Email edited.",
        )

    def test_edit_email(self):
        bot = Bot()
        bot.add_contact(["Joshua", "1110011111"])
        bot.add_contact(["Joshua", "2222222222"])

        record: Record = bot.address_book.find("Joshua")
        self.assertEqual(
            str(record.phones[0]),
            "1110011111",
        )
