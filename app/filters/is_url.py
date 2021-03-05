from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.utils.misc import is_url


@dataclass
class IsUrl(BoundFilter):
    """
    Filtered message should be valid URL.
    """

    key = "is_url"

    is_url: bool

    async def check(self, message: types.Message) -> bool:
        is_url_valid = is_url(message.text)
        return is_url_valid if self.is_url else not is_url_valid
