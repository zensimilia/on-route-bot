import logging

from aiogram import Dispatcher, types
from aiogram.types.callback_query import CallbackQuery

from app.keyboards.settings import (cd_settings, kb_settings,
                                    kb_settings_user_location)


async def settings_show(message: types.Message):
    await message.answer('Персональные настройки пользователя:', reply_markup=kb_settings())


async def settings_get_user_location(cb: types.CallbackQuery):
    """
    Set timezone for user by his location.
    """
    await cb.message.answer("Отправьте своё местоположение для определения часового пояса автоматически.\n", reply_markup=kb_settings_user_location())


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
    dp.register_message_handler(settings_show, commands="settings")
    # dp.register_message_handler(route_start, commands="routeadd", state="*")
    # dp.register_message_handler(route_named, state=CreateRoute.name)
    dp.register_callback_query_handler(
        process_callback_settings, cd_settings.filter())
