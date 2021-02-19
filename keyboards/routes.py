from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import utils.uchar as uchar


def route_buttons(route_id: int, **kwargs) -> InlineKeyboardMarkup:
    """
    Display keyboard for single route. Links to map, weather and edit route keyboard.

    :param int route_id: Active route id.
    :param kwargs: Additional parameters `route_url` and `weather_url` for display links.
    """
    open_map = InlineKeyboardButton(
        'Маршрут', url=kwargs['route_url'])
    open_weather = InlineKeyboardButton(
        'Погода', url=kwargs['weather_url'])
    edit_route = InlineKeyboardButton(
        f'{uchar.GEAR} Действия с маршрутом', callback_data=f'route_edit_{route_id}'
    )
    all_routes = InlineKeyboardButton(
        'Список маршрутов', switch_inline_query_current_chat='/routes')
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
        route_button = InlineKeyboardButton(
            f'{route[3]}', callback_data=f'route_select_{route[0]}')
        inline_kb.add(route_button)
    return inline_kb
