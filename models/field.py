class Field:
    def __init__(self, value):
        self.value = value

    def get_lower(self):
        return self.value.lower()

    def __str__(self):
        return str(self.value)
