class NotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class CarStatusUnavailableException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class RentalAlreadyEndedException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class DatabaseException(Exception):
    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(message)
        self.original_exception = original_exception

class InputValidationException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
