from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.utils.misc import extract_url


@dataclass
class IsUrlFilter(BoundFilter):
    """Filtered message should be valid URL or contains URL."""

    key = "is_url"
    is_url: bool

    async def check(self, message: types.Message) -> bool:
        is_url_found = extract_url(message.text)
        return (
            bool(is_url_found) if bool(self.is_url) else not bool(is_url_found)
        )
