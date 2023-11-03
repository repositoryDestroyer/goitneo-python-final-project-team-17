from exceptions.address_exists import AddressExists
from exceptions.email_exists import EmailExists
from exceptions.missing_record import MissingRecord
from exceptions.wrong_email_format import WrongEmailFormat
from exceptions.wrong_phone_format import WrongPhoneFormat
from exceptions.wrong_birthday_format import WrongBirthdayFormat
from exceptions.short_search_phrase import ShortSearchPhrase
from exceptions.missing_arguments import MissingArguments


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name"
        except KeyError:
            return "Wrong key"
        except (
            WrongPhoneFormat,
            WrongBirthdayFormat,
            WrongEmailFormat,
            AddressExists,
            EmailExists,
            ShortSearchPhrase,
            MissingRecord,
            MissingArguments,
        ) as e:
            return str(e)
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    return inner
