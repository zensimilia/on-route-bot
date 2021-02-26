import time
from typing import Union

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.callback_query import CallbackQuery

import app.utils.uchar as uchar
from app.keyboards.common import *
from app.keyboards.routes import *
from app.models import Route, User
from app.providers.yandex import YAMParser, YAWParser
from app.utils.exceptions import YAParseError, YARequestError
from app.utils.misc import is_url_valid

from .common import something_went_wrong


class CreateRoute(StatesGroup):
    """
    State class for creating route process.
    """

    name = State()
    url = State()


async def route_start(message: types.Message):
    await message.answer(
        "<code>1/2</code> Пожалуйста, выберите название для нового маршрута.",
        reply_markup=cancel_button(),
    )
    await CreateRoute.name.set()


async def route_named(message: types.Message, state: FSMContext):
    if message.text[0] == "/" and message.text != "/cancel":
        return
    await state.update_data(name=message.text)
    await CreateRoute.next()
    await message.answer(
        '<code>2/2</code> Теперь пришлите ссылку на страницу маршрута в <a href="https: // maps.yandex.ru/">Яндекс Картах</a>. Скопируйте её из адресной строки или воспользуйтесь кнопкой "поделиться".',
        reply_markup=cancel_button(),
        disable_web_page_preview=True,
    )


async def route_url_set(message: types.Message, state: FSMContext):
    if (
        message.text[0] == "/"
        and message.text != "/cancel"
        or is_url_valid(message.text) is False
    ):
        return
    await state.update_data(url=message.text)
    state_data = await state.get_data()
    current_user = User.get(User.uid == message.from_user.id)
    Route.create(url=state_data["url"],
                 name=state_data["name"], user=current_user)
    await message.answer(
        f"Маршрут \"<b>{state_data['name']}</b>\" добавлен. "
        "\n\nПосмотрите список всех маршрутов командой /routes. "
        "\nДобавьте еще один маршрут командой /routeadd.",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()


async def route_all(message: types.Message):
    """
    Display list of all routes by `/routes` command.
    """
    await route_list(message)


async def route_list(entity: Union[types.Message, types.CallbackQuery]):
    """
    Display all user routes.
    """
    data = User.get(User.uid == entity.from_user.id).routes
    message = entity
    if data.count() == 0:
        await message.answer('У Вас пока нет ни одного маршрута. Вы можете создать новый маршрут при помощи команды /routeadd.')
        return
    if isinstance(entity, types.CallbackQuery):
        await entity.bot.delete_message(
            entity.message.chat.id, entity.message.message_id
        )
        message = entity.message
    await message.answer(
        f"Выберите один из {data.count()} ваших маршрутов.",
        reply_markup=kb_route_list(data),
    )


async def route_show(message: types.Message, route_id: int):
    """
    Show specific route information and action buttons.

    :param obj message: Message object.
    :param int route_id: Route id.
    """
    timestamp = time.ctime()

    # get user route from database
    route = Route.get(Route.id == route_id)

    try:
        yamp = YAMParser(route.url)  # map parser instance
        map_center = yamp.coords

        # weather parser instance
        yawp = YAWParser(map_center["lat"], map_center["lon"])

        temp = yawp.temp + f" {uchar.DEGREE}C"
        fact = yawp.fact + "."
        time_left = yamp.time

        # add timestamp to avoid image caching
        map_url = f"{yamp.map}&{timestamp}"

        inline_buttons = kb_route_buttons(
            route_id, route_url=yamp.url, weather_url=yawp.url
        )

        await message.answer_photo(
            map_url,
            caption=f"<b>Маршрут:</b> {route.name} \n<b>Время в пути:</b> {time_left}. \n<b>Прогноз погоды:</b> {temp} {fact}\n",
            reply_markup=inline_buttons,
        )
        await message.delete()

    except (YAParseError, YARequestError) as e:
        await something_went_wrong(message, e)


async def process_callback_routes(cb: types.CallbackQuery):
    data = cd_routes.parse(cb.data)
    action = data.get("action")
    route_id = data.get("route_id")

    if action == "list":
        await route_list(cb)
    elif action == "show":
        await route_show(cb.message, route_id=int(route_id))
    elif action == "edit":
        await route_edit(cb, route_id=int(route_id))
    elif action == "delete":
        await route_delete(cb, route_id=int(route_id))
    elif action == "delete_no":
        await route_delete_no(cb)
    elif action == "delete_confirm":
        await route_delete_confirm(cb, route_id=int(route_id))


async def route_delete_no(cb: CallbackQuery):
    await cb.message.delete()


async def route_delete_confirm(cb: CallbackQuery, route_id: int):
    """
    Delete route from DB and send message.

    :param int route_id: Route id.
    """
    Route.delete_by_id(route_id)
    await cb.message.delete()
    await cb.message.answer('Маршрут успешно удален. Посмотрите список всех маршрутов командой /routes.')
    pass


async def route_delete(cb: types.CallbackQuery, route_id):
    route_name = Route.get_by_id(route_id).name
    await cb.message.answer(
        f'Вы уверены, что хотите удалить маршрут <b>{route_name}</b>?', reply_markup=kb_route_delete_confirm_buttons(route_id))
    await cb.answer()


async def route_edit(cb: types.CallbackQuery, route_id):
    keyboard = kb_route_edit_buttons(route_id)
    await cb.message.edit_reply_markup(keyboard)
    await cb.answer()


async def process_callback_route_select(callback_query: types.CallbackQuery):
    route_id = callback_query.get("route_id")
    await route_show(callback_query.message, route_id)
    await callback_query.answer()


def register_handlers_routes(dp: Dispatcher):
    """
    Register routes handlers in Dispatcher.
    """
    dp.register_message_handler(route_all, commands="routes")
    dp.register_message_handler(route_start, commands="routeadd", state="*")
    dp.register_message_handler(route_named, state=CreateRoute.name)
    dp.register_message_handler(route_url_set, state=CreateRoute.url)
    dp.register_callback_query_handler(
        process_callback_routes, cd_routes.filter())
