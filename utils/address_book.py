import pickle

from models.address_book import AddressBook


def load_address_book(address_book_filename):
    result = AddressBook()
    try:
        with open(address_book_filename, "rb") as fh:
            existing_data = pickle.load(fh)
            result = existing_data
    except OSError as e:
        return result
    except Exception as e:
        print(e)

    return result


def save_address_book(address_book_filename, address_book_to_save):
    try:
        with open(address_book_filename, "wb") as fh:
            json_string = pickle.dumps(address_book_to_save)
            fh.write(json_string)
    except Exception as e:
        print(e)
