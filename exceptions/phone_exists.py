class PhoneExists(Exception):
    def __init__(self, message="Phone number exists"):
        self.message = message
        super().__init__(self.message)
