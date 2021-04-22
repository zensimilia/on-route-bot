from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery

from app.keyboards import common, inline_route
from app.models import Route, User
from app.states import CreateRoute
from app.db import db_session
from app.utils.misc import extract_url


async def route_add(message: types.Message):
    """Start create new route process."""
    await CreateRoute.name.set()
    await message.answer(
        '<code>1/2</code> Пожалуйста, введите название для нового маршрута.',
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
        'воспользуйтесь кнопкой "поделиться". Используйте промежуточные точки '
        'чтобы задать более точный маршрут, иначе будет выбран более '
        'оптимальный - это может не совпасть с вашими ожиданиями.',
        reply_markup=common.cancel_button(),
        disable_web_page_preview=True,
    )


async def route_add_url(message: types.Message, state: FSMContext):
    """Set route url and create route from state."""
    await state.update_data(url=message.text)
    state_data = await state.get_data()
    url = extract_url(state_data['url'])
    with db_session() as db:
        user = (
            db.query(User).filter(User.uid.__eq__(message.from_user.id)).first()
        )

        route = Route(url=url, name=state_data['name'], user=user)
        db.add(route)
    await state.finish()
    await message.answer(
        f'Маршрут "<b>{route.name}</b>" добавлен.'
        '\nПосмотрите список всех маршрутов и настройте уведомления '
        'командой /routes. \nДобавьте еще один маршрут командой /routeadd.',
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def route_add_error(message: types.Message, state: FSMContext):
    """Handle errors in create route process."""
    current_state = str(await state.get_state()).split(':')[-1]
    text = str()
    if current_state == 'name':
        text = (
            'Это не похоже на название маршрута. '
            'Попробуйте что-нибудь другое.'
        )
    elif current_state == 'url':
        text = (
            'Наверное в ссылке допущена ошибка или '
            'сообщение не содержит ссылку. Проверьте и попробуйте еще раз.'
        )
    text += (
        ' Если вы передумали, нажмите кнопку "Отмена" или введите '
        'команду /cancel.'
    )
    await message.answer(text)


async def route_list(entity: Union[types.Message, types.CallbackQuery]):
    """Display all user routes by command or callback query."""
    message = (
        'У Вас пока нет ни одного маршрута. '
        'Вы можете создать новый маршрут при помощи команды /routeadd.'
    )
    keyboard = None

    with db_session() as db:
        data = (
            db.query(Route)
            .join(User)
            .where(User.uid.__eq__(entity.from_user.id))
            .all()
        )
    if len(data):
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
    """Display single route actions."""
    route_id = callback_data['route_id']
    with db_session() as db:
        route = db.get(Route, route_id)  # type: ignore
        state = route.is_active

        if callback_data['action'] == 'toggle':
            state = route.toggle()
            text = (
                'Уведомления включены'
                if bool(state)
                else 'Уведомления отключены'
            )
            await cb.answer(text)

    await cb.message.edit_text(
        f'Вы выбрали <b>{route.name}</b>.'
        '\nЧто вы хотите сделать с этим маршрутом?',
        reply_markup=inline_route.kb_route_buttons(route_id, state),
    )
    await cb.answer()


async def route_show(cb: types.CallbackQuery, callback_data: dict):
    """Show single route information."""
    # get user route from database
    with db_session() as db:
        route = db.get(Route, callback_data['route_id'])  # type: ignore

    message_text = route.message()
    if not message_text:
        await cb.answer('Что-то пошло не так!', show_alert=True)
    else:
        await cb.message.edit_text(
            message_text,
            reply_markup=inline_route.kb_route_single(route.id),
        )


async def route_delete_confirm(cb: CallbackQuery, callback_data: dict):
    """Delete route from DB and send message."""
    with db_session() as db:
        route = db.get(Route, callback_data['route_id'])  # type: ignore
        db.delete(route)

    await cb.answer(f'Маршрут "{route.name}" успешно удален', show_alert=True)
    await route_list(cb)


async def route_delete(cb: types.CallbackQuery, callback_data: dict):
    """Delete route and cascade schedules."""
    with db_session() as db:
        route = db.get(Route, callback_data['route_id'])  # type: ignore

    await cb.message.edit_text(
        f'Вы уверены, что хотите удалить маршрут <b>{route.name}</b>?',
        reply_markup=inline_route.kb_route_delete_confirm_buttons(
            callback_data['route_id']
        ),
    )
    await cb.answer()
