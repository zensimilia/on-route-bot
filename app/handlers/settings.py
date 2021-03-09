import logging
from typing import Union

from aiogram import Dispatcher, types
from aiogram.types.callback_query import CallbackQuery

from app.keyboards.settings import *
from app.models import User


async def settings_list(entity: Union[types.Message, types.CallbackQuery]):
    """
    Display list of all user settings.
    """
    caption = 'Персональные настройки пользователя:'
    kb = kb_settings()
    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption, reply_markup=kb)
        await entity.answer()
        return

    await entity.answer(caption, reply_markup=kb)


async def settings_tz(cb: CallbackQuery, callback_data: dict):
    user = User.get(User.uid == cb.from_user.id)
    text = f'Ваш часовой пояс <b>{user.timezone}</b>.' if user.timezone else 'Укажите ваш часовой пояс для получения уведомлений в корректное время.'
    await cb.message.edit_text(text, reply_markup=kb_settings_tz())
    await cb.answer()


async def settings_get_user_location(cb: types.CallbackQuery):
    """
    Set timezone for user by his location.
    """
    await cb.message.edit_text("Отправьте своё местоположение для определения часового пояса автоматически.\n", reply_markup=kb_settings_user_location())


async def process_callback_settings(cb: CallbackQuery):
    data = cd_settings.parse(cb.data)
    action = data.get('action')
    print(action)
    await cb.answer()


def register_handlers_settings(dp: Dispatcher):
    """
    Register routes handlers in Dispatcher.
    """
    logging.info('Configuring settings handlers...')
    dp.register_message_handler(settings_list, commands="settings")
    dp.register_callback_query_handler(
        settings_list, cd_settings.filter(action='list'))
    dp.register_callback_query_handler(
        settings_tz, cd_settings.filter(action='tz'))
    # dp.register_callback_query_handler(
    # process_callback_settings, cd_settings.filter())
