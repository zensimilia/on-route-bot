import re
from typing import Optional

from aiogram import types


def is_command(text: str) -> bool:
    """Check if string is telegram command.

    :param str text:
    """
    return text[0] == '/'


def is_url(url: str) -> bool:
    """Check string for valid URL.

    :param str url: URL for validate.
    """
    regex = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?))'
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE,
    )
    return re.match(regex, url) is not None


def is_time(time: str) -> bool:
    """Check string for valid time HH:MM format.

    :param str time:
    """
    regex = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
    return bool(regex.match(time))


async def something_went_wrong(messsage: types.Message, error: str = None):
    """Show error message when exception is raised.

    :param obj message: Message object.
    :param obj error: Error object with `__str__` method.
    """
    if error is None:
        error = 'Что-то пошло не так!'
    text = (
        f'<b>{error}</b> \n'
        'Попробуйте позже или обратитесь к автору бота (ссылка в профиле).'
    )
    await messsage.answer(text)


def extract_url(string: str) -> Optional[str]:
    """Extract URL from string.

    Returns URL (str) or None if no links was found.
    """
    regex = re.compile(r'(https?:\/\/[\w]+\.+[^\s]+)', re.IGNORECASE)
    urls = re.findall(regex, string)
    return next(iter(urls), None)
