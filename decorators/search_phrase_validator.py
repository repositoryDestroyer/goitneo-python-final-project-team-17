from exceptions.short_search_phrase import ShortSearchPhrase


def search_phrase_validator(func):
    def inner(*args, **kwargs):
        search_phrase = args[1][0].strip()

        if len(search_phrase) < 2:
            return str(ShortSearchPhrase())

        return func(*args, **kwargs)

    return inner
