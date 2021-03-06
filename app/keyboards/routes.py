from typing import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

import app.utils.uchar as uchar

cd_routes = CallbackData("routes_menu", "action", "route_id")


def kb_route_buttons(route_id: int) -> InlineKeyboardMarkup:
    """
    Display keyboard for single route. Links to map, weather and edit route keyboard.

    :param int route_id: Active route id.
    """
    cb_edit = cd_routes.new(action="edit", route_id=route_id)
    cb_back = cd_routes.new(action="list", route_id=0)
    cb_refresh = cd_routes.new(action="refresh", route_id=route_id)

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    f'{uchar.GEAR} Настроить',
                    callback_data=cb_edit)
            ],
            [
                InlineKeyboardButton(
                    f'{uchar.BACK_ARROW} Назад',
                    callback_data=cb_back),
                InlineKeyboardButton(
                    f'{uchar.REFRESH} Обновить',
                    callback_data=cb_refresh
                )
            ]
        ]
    )


def kb_route_delete_confirm_buttons(route_id: int) -> InlineKeyboardMarkup:
    cb_yes = cd_routes.new(action="delete_confirm", route_id=route_id)
    cb_back = cd_routes.new(action="delete_no", route_id=route_id)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    f'{uchar.CHECK_MARK} Да',
                    callback_data=cb_yes),
                InlineKeyboardButton(
                    f'{uchar.CROSS_MARK} Нет',
                    callback_data=cb_back)
            ]
        ]
    )


def kb_route_edit_buttons(route_id: int) -> InlineKeyboardMarkup:
    """
    Display keyboard with edit route buttons.

    :param int route_id: Active route id.
    """
    cb_back = cd_routes.new(action="back", route_id=route_id)
    cb_delete = cd_routes.new(action="delete", route_id=route_id)
    cb_shedule = cd_routes.new(action="schedule", route_id=route_id)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    f'{uchar.CLOCK} Уведомления',
                    callback_data=cb_shedule
                )
            ],
            [
                InlineKeyboardButton(
                    f'{uchar.BACK_ARROW} Назад',
                    callback_data=cb_back),
                InlineKeyboardButton(
                    f'{uchar.WASTEBASKET} Удалить',
                    callback_data=cb_delete)
            ]
        ]
    )


def kb_route_list(routes: Iterable) -> InlineKeyboardMarkup:
    """
    Display all user routes.

    :param list routes: List of all routes.
    """
    inline_kb = InlineKeyboardMarkup(row_width=1)
    for route in routes:
        status = uchar.BELL if route.is_active else ''
        callback_data = cd_routes.new(action="show", route_id=route.id)
        route_button = InlineKeyboardButton(
            f'{status} {route.name}',
            callback_data=callback_data)
        inline_kb.add(route_button)
    return inline_kb
