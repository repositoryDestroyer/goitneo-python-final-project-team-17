class WrongBirthdayFormat(Exception):
    def __init__(self, message="Date should be in the next format: DD.MM.YYYY"):
        self.message = message
        super().__init__(self.message)
