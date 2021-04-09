from typing import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from app.models import Route
from app.types import Bell
from app.utils import uchar

cd_routes = CallbackData('routes_menu', 'action', 'route_id')


def kb_route_buttons(route_id: int, is_active: bool) -> InlineKeyboardMarkup:
    """Display keyboard for selected route.

    :param int route_id: Selected route id.
    :param bool is_active: Is route notifications active.
    """
    bell = Bell.by_state(not is_active)
    toggle = (
        'Отключить уведомления' if bool(is_active) else 'Включить уведомления'
    )
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    f'{uchar.EYES} Показать маршрут',
                    callback_data=cd_routes.new(
                        action='show', route_id=route_id
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    f'{uchar.CLOCK} Настроить расписание',
                    callback_data=cd_routes.new(
                        action='schedule', route_id=route_id
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    f'{bell} {toggle}',
                    callback_data=cd_routes.new(
                        action='toggle', route_id=route_id
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    f'{uchar.BACK_ARROW} Назад',
                    callback_data=cd_routes.new(action='list', route_id=False),
                ),
                InlineKeyboardButton(
                    f'{uchar.WASTEBASKET} Удалить',
                    callback_data=cd_routes.new(
                        action='delete', route_id=route_id
                    ),
                ),
            ],
        ]
    )


def kb_route_delete_confirm_buttons(route_id: int) -> InlineKeyboardMarkup:
    """Return keyboard with delete route confirmation buttons YES/NO.

    :param int route_id: Selected route id.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    'ДА',
                    callback_data=cd_routes.new(
                        action='delete_confirm', route_id=route_id
                    ),
                ),
                InlineKeyboardButton(
                    'НЕТ',
                    callback_data=cd_routes.new(
                        action='delete_no', route_id=route_id
                    ),
                ),
            ]
        ]
    )


def kb_route_single(route_id: int) -> InlineKeyboardMarkup:
    """Return keyboard for single route with back buttons.

    :param int route_id: Selected route id.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    f'{uchar.BACK_ARROW} Назад',
                    callback_data=cd_routes.new(
                        action='select', route_id=route_id
                    ),
                ),
                InlineKeyboardButton(
                    f'{uchar.CARDS} Все маршруты',
                    callback_data=cd_routes.new(
                        action='list', route_id=route_id
                    ),
                ),
            ]
        ]
    )


def kb_route_list(routes: Iterable[Route]) -> InlineKeyboardMarkup:
    """Display all user routes."""
    kb = list()

    for route in routes:
        bell = Bell.by_state(route.is_active)
        cb_data = cd_routes.new(action='select', route_id=route.id)
        kb.append(
            [
                InlineKeyboardButton(
                    f'{bell} {route.name}', callback_data=cb_data
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=kb)
