from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.utils.misc import is_time


@dataclass
class IsTime(BoundFilter):
    """
    Filtered message should be valid time in HH:MM format.
    """

    key = "is_time"

    is_time: bool

    async def check(self, message: types.Message) -> bool:
        is_time_valid = is_time(message.text)
        return is_time_valid if self.is_time else not is_time_valid
