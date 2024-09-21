

class BaseException(Exception):

    def __int__(self, message):
        self.message = message


class AmadeusException(BaseException):
    ERROR_CODE = "EXT-ERROR-AMDS"

    def __init__(self, message):
        self.message = message


class ValidationException(BaseException):
    ERROR_CODE = "API_VALIDATION_ERROR"

    def __init__(self, message):
        self.message = message


class HttpException(BaseException):
    ERROR_CODE = "EXT-ERROR"
    def __init__(self, message):
        self.message = message
