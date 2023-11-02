class MissingRecord(Exception):
    def __init__(self, message="Contact was not found. Add user first"):
        self.message = message
        super().__init__(self.message)
