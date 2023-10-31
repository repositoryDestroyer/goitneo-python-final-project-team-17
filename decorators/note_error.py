from models.name import Name
from models.note import Notes


def note_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError as e:
            return '{}'.format(e)
        except KeyError:
            return 'There is no such contact.'
        except TypeError as e:
            return 'You got TypeError {}'.format(e)
        except Exception as e:
            return 'Unexpected error: {str({})}'.format(e)
    return inner
