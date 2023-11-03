from exceptions.missing_arguments import MissingArguments


def arguments_validator(expected_args):
    def func_wrapper(func):
        def inner(*args, **kwargs):
            input = args[1]

            if len(input) < len(expected_args):
                return str(MissingArguments(expected_args=expected_args))

            return func(*args, **kwargs)

        return inner

    return func_wrapper
