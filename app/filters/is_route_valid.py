from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter

from app.utils.misc import is_url_valid


@dataclass
class IsRouteVaildFilter(BoundFilter):
    """
    Filtered message should be valid for create route process.
    """

    key = "is_route_valid"

    async def check(self, message: types.Message) -> bool:
        return message.text[0] != '/'
