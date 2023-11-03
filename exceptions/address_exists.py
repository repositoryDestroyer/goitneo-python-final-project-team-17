class AddressExists(Exception):
    def __init__(self, message="Address exists"):
        self.message = message
        super().__init__(self.message)
