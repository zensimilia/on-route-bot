class YAParseError(Exception):
    """
    Raised when parser can't return necessary result.
    """
    pass


class YARequestError(Exception):
    """
    Raised when parser have problems with request document.
    """
    pass
