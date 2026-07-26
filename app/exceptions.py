class EmailAlreadyExistsException(Exception):
    def __init__(self, message="Email already exists"):
        self.message = message
        super().__init__(self.message)
