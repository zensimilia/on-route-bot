from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import utils.uchar as uchar
from aiogram.utils.callback_data import CallbackData

cd_routes = CallbackData("routes_menu", "action", "route_id")


def route_buttons(route_id: int, **kwargs) -> InlineKeyboardMarkup:
    """
    Display keyboard for single route. Links to map, weather and edit route keyboard.

    :param int route_id: Active route id.
    :param kwargs: Additional parameters `route_url` and `weather_url` for display links.
    """
    cb_edit = cd_routes.new(action="edit", route_id=route_id)
    cb_back = cd_routes.new(action="list", route_id=0)
    open_map = InlineKeyboardButton(
        'Маршрут', url=kwargs['route_url'])
    open_weather = InlineKeyboardButton(
        'Погода', url=kwargs['weather_url'])
    edit_route = InlineKeyboardButton(
        f'{uchar.GEAR} Действия с маршрутом', callback_data=cb_edit
    )
    all_routes = InlineKeyboardButton(
        f'{uchar.BACK_ARROW} Назад к списку маршрутов', callback_data=cb_back)
    inline_kb = InlineKeyboardMarkup()
    inline_kb.row(open_map, open_weather)
    inline_kb.add(edit_route)
    inline_kb.add(all_routes)
    return inline_kb


def route_edit_buttons(route_id: int, **kwargs) -> InlineKeyboardMarkup:
    """
    Display keyboard with edit route buttons.

    :param int route_id: Active route id.
    """
    delete_route = InlineKeyboardButton(
        f'{uchar.WASTEBASKET} Удалить маршрут', callback_data=f'route_delete_{route_id}')
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(delete_route)
    return inline_kb


def route_list(routes: list) -> InlineKeyboardMarkup:
    """
    Display all user routes.

    :param list routes: List of all routes.
    """
    inline_kb = InlineKeyboardMarkup(row_width=1)
    for route in routes:
        callback_data = cd_routes.new(action="show", route_id=route[0])
        route_button = InlineKeyboardButton(
            f'{route[3]}', callback_data=callback_data)
        inline_kb.add(route_button)
    return inline_kb
