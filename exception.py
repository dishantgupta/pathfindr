

class BaseException(Exception):

    def __int__(self, message):
        self.message = message


class AmadeusException(BaseException):
    ERROR_CODE = "EXT-ERROR-AMDS"

    def __init__(self, message):
        self.message = message


class ValidationException(BaseException):
    def __init__(self, message):
        self.message = message


class HttpException(BaseException):
    def __init__(self, message):
        self.message = message
