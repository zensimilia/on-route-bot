import re


def is_url_valid(url: str):
    """
    Check string for valid URL.

    :param str url: URL for validate.
    """
    regex = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None
