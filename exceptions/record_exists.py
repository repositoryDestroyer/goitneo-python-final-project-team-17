class RecordExists(Exception):
    def __init__(self, message="Contact exists"):
        self.message = message
        super().__init__(self.message)
