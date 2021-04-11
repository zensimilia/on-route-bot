from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


@dataclass
class IsNameFilter(BoundFilter):
    """
    Filtered message should or not be starts with special characters.
    """

    key = 'is_name'
    is_name: bool

    async def check(self, message: types.Message) -> bool:
        # fmt: off
        chars = ['/', '@', '#', '!', '%', '&', '\\',
                 '*', '^', '$', '~', '`', '"', '\'']
        # fmt: on
        return (
            message.text[0] not in chars
            if bool(self.is_name)
            else message.text[0] in chars
        )
