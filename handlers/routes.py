import time

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import keyboards.common as keyboards
import models.db as db
import utils.uchar as uchar
from mod.parser import YAMParser, YAParseError, YARequestError, YAWParser

from .common import something_went_wrong


class CreateRoute(StatesGroup):
    """
    State class for creating route process.
    """
    name = State()
    url = State()


async def route_start(message: types.Message):
    db.register_user(message.from_user.id, message.from_user.username)
    await message.answer("<code>1/2</code> Введите имя маршрута. Например: дом-дача.", reply_markup=keyboards.cancel_button())
    await CreateRoute.name.set()


async def route_named(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await CreateRoute.next()
    await message.answer("<code>2/2</code> Вставьте ссылку на маршрут в Яндекс картах.", reply_markup=keyboards.cancel_button())


async def route_url_set(message: types.Message, state: FSMContext):
    # [ ] проверить url на валидность `message.text.lower()`
    # [x] добавить в базу маршрут
    # [x] сообщить что все хорошо
    await state.update_data(url=message.text.lower())
    state_data = await state.get_data()
    db.add_route(message.from_user.id, state_data['url'], state_data['name'])
    await message.answer(f"Маршрут \"<b>{state_data['name']}</b>\" добавлен. \nПосмотреть список всех маршрутов /routes \nДобавить еще маршрут /routeadd", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def route_list(message: types.Message):
    """
    Display all user routes.
    """
    data = db.get_routes(message.from_user.id)
    if data is None:
        await message.answer('У вас нет сохраненных маршрутов. \nЧтобы добавить маршрут введите команду /routeadd')
        return
    await message.answer('Ваши сохранённые маршруты:', reply_markup=keyboards.route_list(data))


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

        inline_buttons = keyboards.route_buttons(
            route_id,
            route_url=yamp.url,
            weather_url=yawp.url)

        await message.answer_photo(
            map_url,
            caption=f'<b>Маршрут:</b> {route[3]} \n<b>Время в пути:</b> {time_left}. \n<b>Прогноз погоды:</b> {temp} {fact}\n',
            reply_markup=inline_buttons)

    except (YAParseError, YARequestError) as e:
        await something_went_wrong(message, e)


async def process_callback_route_edit(callback_query: types.CallbackQuery):
    route_id = callback_query.data.split('_')[-1]
    # await bot.answer_callback_query(
    #     callback_query.id,
    #     text=f'route_id: {route_id}', show_alert=True)
    # await bot.answer_callback_query(callback_query.id)
    # await bot.send_message(callback_query.from_user.id, f'Редактировать маршрут {route_id}')
    # await callback_query.answer(f'Редактировать маршрут {route_id}')
    await callback_query.message.answer(callback_query.from_user.id, f'Редактировать маршрут {route_id}', reply_markup=keyboards.route_edit_buttons(route_id))


async def process_callback_route_select(callback_query: types.CallbackQuery):
    route_id = callback_query.data.split('_')[-1]
    await route_show(callback_query.message, route_id)
    await callback_query.answer()


def register_handlers_routes(dp: Dispatcher):
    """
    Register routes handlers in Dispatcher.
    """
    dp.register_message_handler(route_list, commands="routes")
    dp.register_message_handler(route_start, commands="routeadd", state="*")
    dp.register_message_handler(route_named, state=CreateRoute.name)
    dp.register_message_handler(route_url_set, state=CreateRoute.url)
    dp.register_callback_query_handler(
        process_callback_route_edit, lambda c: c.data and c.data.startswith('route_edit_'))
    dp.register_callback_query_handler(
        process_callback_route_select, lambda c: c.data and c.data.startswith('route_select_'))
