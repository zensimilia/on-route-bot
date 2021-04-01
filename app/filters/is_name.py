from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


@dataclass
class IsName(BoundFilter):
    """
    Filtered message should or not be starts with special characters.
    """

    key = 'is_name'
    is_name: bool

    async def check(self, message: types.Message) -> bool:
        chars = ['/', '@', '#', '!', '%', '&',
                 '*', '^', '$', '~', '`', '"', '\'']
        return message.text[0] not in chars and self.is_name
