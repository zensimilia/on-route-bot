import logging
from typing import Union

from aiogram import Dispatcher, types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types.callback_query import CallbackQuery

from app.keyboards.settings import *
from app.models import User
from app.states import SetTimezone


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
    text = f'Ваш часовой пояс <b>{user.timezone}</b>.' if user.timezone else 'Вы не указали свой часовой пояс. Будет использован по умолчанию <b>UTC+3</b> время Московское.'
    await cb.message.edit_text(text, reply_markup=kb_settings_tz())
    await cb.answer()


async def settings_tz_change(cb: types.CallbackQuery):
    """
    Set timezone for user by his location.
    """
    await SetTimezone.tz.set()
    await cb.message.edit_text('Пожалуйста, укажите ваш часовой пояс в формате <code>UTC</code>.'
                               '\n<a href="https://ru.wikipedia.org/wiki/%D0%92%D1%81%D0%B5%D0%BC%D0%B8%D1%80%D0%BD%D0%BE%D0%B5_%D0%BA%D0%BE%D0%BE%D1%80%D0%B4%D0%B8%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5_%D0%B2%D1%80%D0%B5%D0%BC%D1%8F">Подробнее</a> о формате.',
                               reply_markup=None,
                               disable_web_page_preview=True)


async def settings_tz_set(message: types.Message, state: FSMContext):
    user = User.get(User.uid == message.from_user.id)
    tz = message.text.split(' ')[0].upper()
    user.update(timezone=tz).execute()
    await message.answer(f'Ваш часовой пояс установлен как <b>{tz}</b>. \nВернуться к списку настроек /settings.')
    await state.finish()


async def settings_tz_error(message: types.Message, state: FSMContext):
    await message.answer('Это не похоже на формат <a href="https://ru.wikipedia.org/wiki/%D0%92%D1%81%D0%B5%D0%BC%D0%B8%D1%80%D0%BD%D0%BE%D0%B5_%D0%BA%D0%BE%D0%BE%D1%80%D0%B4%D0%B8%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5_%D0%B2%D1%80%D0%B5%D0%BC%D1%8F">всемирного координированного времени</a>.', disable_web_page_preview=True)
