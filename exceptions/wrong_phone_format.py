class WrongPhoneFormat(Exception):
    def __init__(self, message="Phone should consist of 10 digits"):
        self.message = message
        super().__init__(self.message)
