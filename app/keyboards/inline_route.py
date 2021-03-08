from app.models import route
from typing import Iterable, List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

import app.utils.uchar as uchar

cd_routes = CallbackData("routes_menu", "action", "route_id")


def kb_route_buttons(route_id: int, is_active: bool) -> InlineKeyboardMarkup:
    """
    Display keyboard for single route. Links to map, weather and edit route keyboard.

    :param int route_id: Active route id.
    :param bool is_active: Is route notifications active.
    """
    status = uchar.BELL if not is_active else uchar.BELL_STROKE
    toggle = 'Отключить уведомления' if is_active else 'Включить уведомления'
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    f'{uchar.EYES} Показать маршрут',
                    callback_data=cd_routes.new(action='show', route_id=route_id))
            ],
            [
                InlineKeyboardButton(
                    f'{uchar.CLOCK} Настроить расписание',
                    callback_data=cd_routes.new(action='schedule', route_id=route_id)),
            ],
            [
                InlineKeyboardButton(
                    f'{status} {toggle}',
                    callback_data=cd_routes.new(action='toggle', route_id=route_id))
            ],
            [
                InlineKeyboardButton(
                    f'{uchar.BACK_ARROW} Назад',
                    callback_data=cd_routes.new(action='list', route_id=False)),
                InlineKeyboardButton(
                    f'{uchar.WASTEBASKET} Удалить',
                    callback_data=cd_routes.new(action='delete', route_id=route_id))
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


def kb_route_single(route_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    f'{uchar.BACK_ARROW} Назад',
                    callback_data=cd_routes.new(action='select', route_id=route_id)),
                InlineKeyboardButton(
                    f'{uchar.CARDS} Все маршруты',
                    callback_data=cd_routes.new(action='list', route_id=route_id)),
            ]
        ]
    )


def kb_route_list(routes: Iterable) -> InlineKeyboardMarkup:
    """
    Display all user routes.

    :param list routes: List of all routes.
    """
    kb = list()

    for route in routes:
        status = uchar.CIRCLE_GREEN if route.is_active else uchar.CIRCLE_RED
        cb_data = cd_routes.new(action="select", route_id=route.id)
        kb.append([
            InlineKeyboardButton(
                f'{status} {route.name}',
                callback_data=cb_data)
        ])
    return InlineKeyboardMarkup(inline_keyboard=kb)
