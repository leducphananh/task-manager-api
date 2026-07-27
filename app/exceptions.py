class AppException(Exception):
    """Base class for all application-specific exceptions"""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class EmailAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(status_code=409, message="Email already exists")


class InvalidCredentialsException(AppException):
    def __init__(self):
        super().__init__(status_code=401, message="Invalid credentials")


class InvalidTokenException(AppException):
    def __init__(self):
        super().__init__(status_code=401, message="Invalid or expired token")


class TaskNotFoundException(AppException):
    def __init__(self):
        super().__init__(status_code=404, message="Task not found")
