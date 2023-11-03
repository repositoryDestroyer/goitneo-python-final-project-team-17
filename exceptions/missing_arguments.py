class MissingArguments(Exception):
    def __init__(self, expected_args=[]):
        message = (
            "Give me next arguments, please: "
            if len(expected_args) >= 2
            else "Give me next argument, please: "
        )
        self.message = f"{message}{', '.join(expected_args)}"
        super().__init__(self.message)
