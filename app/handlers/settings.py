from typing import Union

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from app.keyboards import settings
from app.models import User
from app.states import SetTimezone


async def settings_list(entity: Union[types.Message, types.CallbackQuery]):
    """Display list of all user settings."""
    caption = 'Персональные настройки пользователя:'
    kb = settings.kb_settings()
    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption, reply_markup=kb)
        await entity.answer()
        return

    await entity.answer(caption, reply_markup=kb)


async def settings_tz(cb: CallbackQuery):
    user = User.get(User.uid == cb.from_user.id)
    text = f'Ваш часовой пояс <b>{user.timezone}</b>.' \
        if user.timezone \
        else 'Вы не указали свой часовой пояс. ' \
        'Будет использован по умолчанию <b>UTC+3</b> время Московское.'
    await cb.message.edit_text(text, reply_markup=settings.kb_settings_tz())
    await cb.answer()


async def settings_tz_change(cb: types.CallbackQuery):
    """Set timezone for user by his location."""
    await SetTimezone.tz.set()
    await cb.message.edit_text(
        'Пожалуйста, укажите ваш часовой пояс в формате <code>UTC</code>.'
        '\n<a href="'
        'https://ru.wikipedia.org/wiki/Всемирное_координированное_время'
        '">Подробнее</a> о формате.',
        reply_markup=None,
        disable_web_page_preview=True
    )


async def settings_tz_set(message: types.Message, state: FSMContext):
    user = User.get(User.uid == message.from_user.id)
    tz = message.text.split(' ')[0].upper()
    user.update(timezone=tz).execute()
    await message.answer(
        f'Ваш часовой пояс установлен как <b>{tz}</b>. '
        '\nВернуться к списку настроек /settings.'
    )
    await state.finish()


async def settings_tz_error(message: types.Message):
    await message.answer(
        'Это не похоже на формат <a href="'
        'https://ru.wikipedia.org/wiki/Всемирное_координированное_время">'
        'всемирного координированного времени</a>.',
        disable_web_page_preview=True)
