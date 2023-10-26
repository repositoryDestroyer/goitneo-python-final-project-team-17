from re import S
import unittest
from datetime import datetime, timedelta
from collections import defaultdict

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
        bot = Bot()
        result = bot.add_contact(["John", "8572156295"])
        record: Record = bot.addressBook.find("John")

        self.assertEqual(record.phones[0].value, "8572156295")
        self.assertEqual(result, "Contact added.")

    def test_add_contact_wrong_args(self):
        bot = Bot()
        result = bot.add_contact([])

        self.assertEqual(len(bot.addressBook) == 0, True)
        self.assertEqual(result, "Give me name and phone please.")

    def test_change_contact_happy_flow(self):
        bot = Bot()
        bot.add_contact(["John", "1234569012"])

        result = bot.change_contact(["John", "9999999999"])
        record: Record = bot.addressBook.find("John")

        self.assertEqual(record.phones[0].value, "9999999999")
        self.assertEqual(result, "Contact updated.")

    def test_change_contact_not_found(self):
        bot = Bot()
        bot.add_contact(["Joshua", "1234569012"])
        result = bot.change_contact([])
        record: Record = bot.addressBook.find("Joshua")

        self.assertEqual(record.phones[0].value, "1234569012")
        self.assertEqual(result, "Give me name and phone please.")

    def test_change_contact_wrong_args(self):
        bot = Bot()
        bot.add_contact(["Johan", "1234511111"])
        result = bot.change_contact(["Jack", "9999999999"])

        self.assertEqual(result, "Contact was not found.")

    def test_show_phone_happy_flow(self):
        bot = Bot()
        bot.add_contact(["Joshua", "1114511111"])
        result = bot.show_phone(["Joshua"])

        self.assertEqual(str(result), "Contact name: Joshua, phones: 1114511111")

    def test_show_phone_not_found(self):
        bot = Bot()
        bot.add_contact(["Joshua", "1114511111"])
        result = bot.show_phone(["Vasyl"])

        self.assertEqual(result, "Contact was not found.")

    def test_show_phone_wrond_args(self):
        bot = Bot()
        bot.add_contact(["Joshua", "1110011111"])
        result = bot.show_phone([])
        record: Record = bot.addressBook.find("Joshua")

        self.assertEqual(record.phones[0].value, "1110011111")
        self.assertEqual(result, "Enter user name")

    def test_show_all(self):
        bot = Bot()
        bot.add_contact(["Joshua", "1110011111"])
        bot.add_contact(["Steve", "2928274219"])
        result = bot.show_all()

        self.assertEqual(
            str(result),
            "Contact name: Joshua, phones: 1110011111\nContact name: Steve, phones: 2928274219",
        )
