import time

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import keyboards.common
import keyboards.routes
import models.db as db
import utils.uchar as uchar
from providers.yandex import YAMParser, YAWParser
from utils.exceptions import YARequestError, YAParseError
from utils.misc import is_url_valid
from keyboards.routes import cd_routes

from .common import something_went_wrong

from typing import Union


class CreateRoute(StatesGroup):
    """
    State class for creating route process.
    """
    name = State()
    url = State()


async def route_start(message: types.Message):
    await message.answer("<code>1/2</code> Введите имя маршрута. Например: <i>Дом-дача</i> или <i>Пробка на Мира</i>.", reply_markup=keyboards.common.cancel_button())
    await CreateRoute.name.set()


async def route_named(message: types.Message, state: FSMContext):
    if message.text[0] == '/' and message.text != '/cancel':
        return
    await state.update_data(name=message.text)
    await CreateRoute.next()
    await message.answer("<code>2/2</code> Вставьте ссылку на страницу маршрута в <a href='https://maps.yandex.ru/'>Яндекс Картах</a>.",
                         reply_markup=keyboards.common.cancel_button(),
                         disable_web_page_preview=True)


async def route_url_set(message: types.Message, state: FSMContext):
    if message.text[0] == '/' and message.text != '/cancel' or is_url_valid(message.text) is False:
        return
    await state.update_data(url=message.text)
    state_data = await state.get_data()
    db.add_route(message.from_user.id, state_data['url'], state_data['name'])
    await message.answer(f"Маршрут \"<b>{state_data['name']}</b>\" добавлен. "
                         "\n\nПосмотреть список всех маршрутов /routes "
                         "\nДобавить новый маршрут /routeadd",
                         reply_markup=types.ReplyKeyboardRemove())
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
    data = db.get_routes(entity.from_user.id)
    # if data is None:
    # await message.answer('У вас нет сохраненных маршрутов. \nЧтобы добавить маршрут введите команду /routeadd')
    # return
    # if isinstance(message, types.Message):
    # await message.answer('Выберите маршрут из списка ниже:', reply_markup=keyboards.routes.route_list(data))
    message = entity
    if isinstance(entity, types.CallbackQuery):
        await entity.bot.delete_message(entity.message.chat.id, entity.id)
        message = entity.message
    await message.answer('Выберите маршрут из списка ниже:', reply_markup=keyboards.routes.route_list(data))
    # else:
    # await message.message.edit_reply_markup(keyboards.routes.route_list(data))


async def route_show(message: types.Message, route_id: int):
    """
    Show specific route information and action buttons.

    :param obj message: Message object.
    :param int route_id: Route id.
    """
    timestamp = time.ctime()

    # get user route from database
    route = db.get_routes(message.from_user.id, route_id)[0]

    try:
        yamp = YAMParser(route[2])  # map parser instance
        map_center = yamp.coords

        # weather parser instance
        yawp = YAWParser(map_center['lat'], map_center['lon'])

        temp = yawp.temp + f' {uchar.DEGREE}C'
        fact = yawp.fact + '.'
        time_left = yamp.time

        # add timestamp to avoid image caching
        map_url = f'{yamp.map}&{timestamp}'

        inline_buttons = keyboards.routes.route_buttons(
            route_id,
            route_url=yamp.url,
            weather_url=yawp.url)

        await message.answer_photo(
            map_url,
            caption=f'<b>Маршрут:</b> {route[3]} \n<b>Время в пути:</b> {time_left}. \n<b>Прогноз погоды:</b> {temp} {fact}\n',
            reply_markup=inline_buttons)
        await message.delete()

    except (YAParseError, YARequestError) as e:
        await something_went_wrong(message, e)


async def process_callback_routes(cb: types.CallbackQuery):
    data = cd_routes.parse(cb.data)
    action = data.get('action')
    route_id = data.get('route_id')

    if action == 'list':
        await route_list(cb)
    elif action == 'show':
        await route_show(cb.message, route_id=int(route_id))


async def process_callback_route_edit(callback_query: types.CallbackQuery):
    route_id = callback_query.data.split('_')[-1]
    await callback_query.message.answer(f'Редактировать маршрут {route_id}', reply_markup=keyboards.routes.route_edit_buttons(route_id))
    await callback_query.answer()


async def process_callback_route_select(callback_query: types.CallbackQuery):
    route_id = callback_query.get('route_id')
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
