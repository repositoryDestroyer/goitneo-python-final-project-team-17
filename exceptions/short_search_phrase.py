class ShortSearchPhrase(Exception):
    def __init__(
        self, message="Search phrase is too short. It should contain at least 2 chars."
    ):
        self.message = message
        super().__init__(self.message)
