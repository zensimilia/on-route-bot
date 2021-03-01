from typing import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

import app.utils.uchar as uchar

cd_routes = CallbackData("routes_menu", "action", "route_id")


def kb_route_buttons(route_id: int, **kwargs) -> InlineKeyboardMarkup:
    """
    Display keyboard for single route. Links to map, weather and edit route keyboard.

    :param int route_id: Active route id.
    :param kwargs: Additional parameters `route_url` and `weather_url` for display links.
    """
    cb_edit = cd_routes.new(action="edit", route_id=route_id)
    cb_back = cd_routes.new(action="list", route_id=0)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Маршрут', url=kwargs['route_url']),
                InlineKeyboardButton('Погода', url=kwargs['weather_url'])
            ],
            [InlineKeyboardButton(
                f'{uchar.GEAR} Действия с маршрутом',
                callback_data=cb_edit)
             ],
            [InlineKeyboardButton(
                f'{uchar.BACK_ARROW} Назад к списку маршрутов',
                callback_data=cb_back)
             ]
        ]
    )


def kb_route_delete_confirm_buttons(route_id: int) -> InlineKeyboardMarkup:
    cb_yes = cd_routes.new(action="delete_confirm", route_id=route_id)
    cb_back = cd_routes.new(action="delete_no", route_id=route_id)
    reply_kb = InlineKeyboardMarkup()
    yes_button = InlineKeyboardButton(
        f'{uchar.CHECK_MARK} Да', callback_data=cb_yes)
    no_button = InlineKeyboardButton(
        f'{uchar.CROSS_MARK} Нет', callback_data=cb_back)
    reply_kb.row(yes_button, no_button)
    return reply_kb


def kb_route_edit_buttons(route_id: int) -> InlineKeyboardMarkup:
    """
    Display keyboard with edit route buttons.

    :param int route_id: Active route id.
    """
    cb_back = cd_routes.new(action="show", route_id=route_id)
    cb_delete = cd_routes.new(action="delete", route_id=route_id)
    delete_route = InlineKeyboardButton(
        f'{uchar.WASTEBASKET} Удалить маршрут', callback_data=cb_delete)
    all_routes = InlineKeyboardButton(
        f'{uchar.BACK_ARROW} Назад к маршруту', callback_data=cb_back)
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(delete_route)
    inline_kb.add(all_routes)
    return inline_kb


def kb_route_list(routes: Iterable) -> InlineKeyboardMarkup:
    """
    Display all user routes.

    :param list routes: List of all routes.
    """
    inline_kb = InlineKeyboardMarkup(row_width=1)
    for route in routes:
        callback_data = cd_routes.new(action="show", route_id=route.id)
        route_button = InlineKeyboardButton(
            f'{route.name}', callback_data=callback_data)
        inline_kb.add(route_button)
    return inline_kb
