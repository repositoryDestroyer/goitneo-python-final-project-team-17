from exceptions.wrong_phone_format import WrongPhoneFormat
from exceptions.wrong_birthday_format import WrongBirthdayFormat


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
        except (WrongPhoneFormat, WrongBirthdayFormat) as e:
            return e
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    return inner
