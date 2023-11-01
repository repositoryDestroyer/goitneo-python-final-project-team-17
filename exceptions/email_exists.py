class EmailExists(Exception):
    def __init__(self, message="Email exists"):
        self.message = message
        super().__init__(self.message)
