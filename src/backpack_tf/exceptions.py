class BackpackTFException(Exception):
    pass


class NoTokenProvided(BackpackTFException):
    pass


class NeedsAPIKey(BackpackTFException):
    pass


class InvalidIntent(BackpackTFException):
    pass


class UserNotFound(BackpackTFException):
    pass


class InvalidAssetID(BackpackTFException):
    pass


class InvalidSKU(BackpackTFException):
    pass
