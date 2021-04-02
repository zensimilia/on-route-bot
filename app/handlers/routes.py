import time
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.markdown import hide_link


from app.utils import uchar
from app.keyboards import common, inline_route
from app.models import Route, User
from app.providers.yandex import (
    YAMParser,
    YAParseError,
    YARequestError,
    YAWParser,
)
from app.states import CreateRoute
from app.utils.misc import something_went_wrong


async def route_add(message: types.Message):
    """Start create new route process."""
    await CreateRoute.name.set()
    await message.answer(
        '<code>1/2</code> Пожалуйста, выберите название для нового маршрута.',
        reply_markup=common.cancel_button(),
    )


async def route_add_name(message: types.Message, state: FSMContext):
    """Set route name to state and send message url request."""
    await state.update_data(name=message.text)
    await CreateRoute.next()
    await message.answer(
        '<code>2/2</code> Теперь пришлите ссылку на страницу маршрута в '
        '<a href="https://maps.yandex.ru/">Яндекс Картах</a>. '
        'Скопируйте её из адресной строки или '
        'воспользуйтесь кнопкой "поделиться".',
        reply_markup=common.cancel_button(),
        disable_web_page_preview=True,
    )


async def route_add_url(message: types.Message, state: FSMContext):
    """
    Set route url and create route from state.
    """
    await state.update_data(url=message.text)
    state_data = await state.get_data()
    current_user = User.get(User.uid == message.from_user.id)
    Route.create(
        url=state_data['url'], name=state_data['name'], user=current_user
    )
    await message.answer(
        f'Маршрут "<b>{state_data["name"]}</b>" добавлен.'
        '\n\nПосмотрите список всех маршрутов командой /routes.'
        '\nДобавьте еще один маршрут командой /routeadd.',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()


async def route_add_error(message: types.Message, state: FSMContext):
    """
    Handle errors in create route process.
    """
    current_state = str(await state.get_state()).split(':')[-1]
    if current_state == 'name':
        await message.answer(
            'Это не похоже на название маршрута. Попробуйте что-нибудь другое.'
        )
    elif current_state == 'url':
        await message.answer(
            'Наверное в ссылке допущена ошибка. Проверьте и попробуйте еще раз.'
        )


async def route_list(entity: Union[types.Message, types.CallbackQuery]):
    """
    Display all user routes by command or callback query.
    """
    message = (
        'У Вас пока нет ни одного маршрута. '
        'Вы можете создать новый маршрут при помощи команды /routeadd.'
    )
    keyboard = None

    data = User.get(User.uid == entity.from_user.id).routes
    if data.count():
        message = 'Выберите маршрут из списка ниже:'
        keyboard = inline_route.kb_route_list(data)

    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(message, reply_markup=keyboard)
        await entity.answer()
        return

    await entity.answer(
        message,
        reply_markup=keyboard,
    )


async def route_select(cb: types.CallbackQuery, callback_data: dict):
    """
    Display selected route with keyboard.
    """
    route_id = callback_data['route_id']
    route = Route.get_by_id(route_id)
    is_active = route.is_active

    if callback_data['action'] == 'toggle':
        is_active = not is_active
        text = 'Уведомления включены' if is_active else 'Уведомления отключены'
        Route.update(is_active=is_active).where(Route.id == route_id).execute()
        await cb.answer(text)

    await cb.message.edit_text(
        str(
            f'Вы выбрали <b>{route.name}</b>.'
            '\nЧто вы хотите сделать с этим маршрутом?'
        ),
        reply_markup=inline_route.kb_route_buttons(route_id, is_active),
    )
    await cb.answer()


async def route_show(cb: types.CallbackQuery, callback_data: dict):
    """
    Show specific route information and action buttons.

    :param obj message: Message object.
    :param int route_id: Route id.
    """
    timestamp = time.ctime()

    route_id = callback_data['route_id']
    # get user route from database
    route = Route.get_by_id(route_id)

    try:
        yamp = YAMParser(route.url)  # map parser instance
        map_center = yamp.coords

        # weather parser instance
        yawp = YAWParser(map_center['lat'], map_center['lon'])

        temp = yawp.temp + f'{uchar.DEGREE}C'
        fact = yawp.fact
        time_left = yamp.time

        # add timestamp to avoid image caching
        map_url = hide_link(f'{yamp.map}&{timestamp}')

        await cb.message.edit_text(
            str(
                f'{map_url}'
                f'Маршрут <b>{route.name}</b> займет <b>{time_left}</b> '
                '<a href="{yamp.url}">(открыть)</a>. '
                f'За окном <b>{temp}</b> {fact} '
                '<a href="{yawp.url}">(подробнее)</a>.'
            ),
            reply_markup=inline_route.kb_route_single(route_id),
        )
        await cb.answer()

    except (YAParseError, YARequestError) as e:
        await something_went_wrong(cb.message, e)


async def route_delete_confirm(cb: CallbackQuery, callback_data: dict):
    """
    Delete route from DB and send message.

    :param int route_id: Route id.
    """
    route_id = callback_data['route_id']

    route = Route.get_by_id(route_id)
    route.delete_instance(recursive=True)

    await cb.message.edit_text(
        f'Маршрут <b>{route.name}</b> успешно удален {uchar.OK_HAND}'
        '\n\nПосмотрите список всех маршрутов командой /routes.'
        '\nИли создайте новый маршрут командой /routeadd.'
    )
    await cb.answer()


async def route_delete(cb: types.CallbackQuery, callback_data: dict):
    """Delete route and cascade schedules."""
    route_id = callback_data['route_id']
    route = Route.get_by_id(route_id)
    await cb.message.edit_text(
        f'Вы уверены, что хотите удалить маршрут <b>{route.name}</b>?',
        reply_markup=inline_route.kb_route_delete_confirm_buttons(route_id),
    )
    await cb.answer()
