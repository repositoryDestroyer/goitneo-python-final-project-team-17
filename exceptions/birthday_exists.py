class BirthdayExists(Exception):
    def __init__(self, message="Birthday exists"):
        self.message = message
        super().__init__(self.message)
