import logging
import time
from re import split
from typing import Union

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery

import app.utils.uchar as uchar
from app.keyboards.common import *
from app.keyboards.routes import *
from app.models import Route, User
from app.providers.yandex import (YAMParser, YAParseError, YARequestError,
                                  YAWParser)
from app.states import CreateRoute, CreateSchedule
from app.utils.misc import is_time_format, is_url, something_went_wrong


async def route_add(message: types.Message):
    """
    Start create new route process.
    """
    await CreateRoute.name.set()
    await message.answer(
        "<code>1/2</code> Пожалуйста, выберите название для нового маршрута.",
        reply_markup=cancel_button(),
    )


async def route_add_name(message: types.Message, state: FSMContext):
    """
    Set route name to state and send message url request.
    """
    await state.update_data(name=message.text)
    await CreateRoute.next()
    await message.answer(
        '<code>2/2</code> Теперь пришлите ссылку на страницу маршрута в <a href="https://maps.yandex.ru/">Яндекс Картах</a>. Скопируйте её из адресной строки или воспользуйтесь кнопкой "поделиться".',
        reply_markup=cancel_button(),
        disable_web_page_preview=True,
    )


async def route_add_url(message: types.Message, state: FSMContext):
    """
    Set route url and create route from state.
    """
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


async def route_add_error(message: types.Message, state: FSMContext):
    """
    Handle errors in create route process.
    """
    current_state = split(':', await state.get_state())[-1]
    if current_state == 'name':
        await message.answer('Это не похоже на название маршрута. Попробуйте что-нибудь другое.')
    elif current_state == 'url':
        await message.answer('Наверное в ссылке допущена ошибка. Проверьте и попробуйте еще раз.')


async def route_list(entity: Union[types.Message, types.CallbackQuery]):
    """
    Display all user routes by command or callback query.
    """
    message = 'У Вас пока нет ни одного маршрута. Вы можете создать новый маршрут при помощи команды /routeadd.'
    keyboard = None

    data = User.get(User.uid == entity.from_user.id).routes
    if data.count():
        message = f"Выберите один из ваших маршрутов."
        keyboard = kb_route_list(data)

    if isinstance(entity, types.CallbackQuery):
        entity = entity.message
        await entity.delete()

    await entity.answer(
        message,
        reply_markup=keyboard,
    )


async def route_show(cb: types.CallbackQuery, route_id: int, back: bool = None):
    """
    Show specific route information and action buttons.

    :param obj message: Message object.
    :param int route_id: Route id.
    """
    if back:
        await cb.message.edit_reply_markup(kb_route_buttons(route_id))
        return

    timestamp = time.ctime()

    # get user route from database
    route = Route.get(Route.id == route_id)

    try:
        yamp = YAMParser(route.url)  # map parser instance
        map_center = yamp.coords

        # weather parser instance
        yawp = YAWParser(map_center["lat"], map_center["lon"])

        temp = yawp.temp + f"{uchar.DEGREE}C"
        fact = yawp.fact
        time_left = yamp.time

        # add timestamp to avoid image caching
        map_url = f"{yamp.map}&{timestamp}"

        await cb.message.answer_photo(
            map_url,
            caption=str(f'Маршрут <b>"{route.name}"</b> займет <b>{time_left}</b> <a href="{yamp.url}">(открыть)</a>. '
                        f'За окном <b>{temp}</b> {fact} <a href="{yawp.url}">(подробнее)</a>.'),
            reply_markup=kb_route_buttons(route_id),
        )
        await cb.message.delete()

    except (YAParseError, YARequestError) as e:
        await something_went_wrong(cb.message, e)


async def process_callback_routes(cb: types.CallbackQuery):
    data = cd_routes.parse(cb.data)
    action, route_id = data['action'], data['route_id']

    if action == "list":
        await route_list(cb)
    elif action in ["show", "refresh"]:
        await route_show(cb, route_id=int(route_id))
    elif action == "back":
        await route_show(cb, route_id=int(route_id), back=True)
    elif action == "edit":
        await route_edit(cb, route_id=int(route_id))
    elif action == "delete":
        await route_delete(cb, route_id=int(route_id))
    elif action == "delete_no":
        await route_delete_no(cb)
    elif action == "delete_confirm":
        await route_delete_confirm(cb, route_id=int(route_id))
    elif action == "schedule":
        await route_edit_schedule(cb, route_id=route_id)


async def route_edit_schedule(cb: types.CallbackQuery, route_id: int):
    await cb.message.answer(
        '<code>1/2</code> Пожалуйста, введите желаемое время уведомления о маршруте в формате <code>ЧЧ:ММ</code>.')
    await CreateSchedule.time.set()


async def route_schedule_time_set(message: types.Message, state: FSMContext):
    if message.text[0] == "/" and message.text != "/cancel":
        return
    if is_time_format(message.text):
        await state.update_data(time=message.text)
        await CreateSchedule.next()
        await message.answer('<code>2/2</code> Теперь выберите дни, в которые надо получать уведомления.', reply_markup=kb_schedule_days())
    return


async def route_delete_no(cb: types.CallbackQuery):
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


async def process_callback_route_select(cb: types.CallbackQuery):
    route_id = cb.get("route_id")
    await route_show(cb.message, route_id)
    await cb.answer()


def register_handlers_routes(dp: Dispatcher):
    """
    Register routes handlers in Dispatcher.
    """
    logging.info('Configuring routes handlers...')
    dp.register_message_handler(route_list, commands="routes")
    dp.register_message_handler(route_add, commands="routeadd")
    dp.register_message_handler(route_add_name,
                                is_name=True,
                                state=CreateRoute.name)
    dp.register_message_handler(route_add_url,
                                is_url=True,
                                state=CreateRoute.url)
    dp.register_message_handler(route_add_error,
                                is_name=False,
                                is_url=False,
                                state=CreateRoute)
    dp.register_message_handler(
        route_schedule_time_set, state=CreateSchedule.time)
    dp.register_callback_query_handler(
        process_callback_routes, cd_routes.filter())
