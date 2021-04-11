from aiogram import types
from aiogram.dispatcher import FSMContext

from app.db import db_session
from app.models import User
from app.utils import uchar


async def cmd_start(message: types.Message):
    """Show welcome message and register user.

    :param obj message: Message object.
    """
    with db_session() as db:
        user = User(
            uid=message.from_user.id, username=message.from_user.username
        )
        db.add(user)
    await message.answer('Welcome text!')  # todo: change welcome text


async def cmd_about(message: types.Message):
    """Show information about bot."""
    await message.answer(
        'Hi! I\'m the <b>Traffic Assistant Bot</b>. '
        '\nI will warn you about traffic jams and weather '
        'forecast on your route by schedule. '
        '\nI\'am work yet with '
        '<a href="https://maps.yandex.com">Yandex Maps</a> only.',
        disable_web_page_preview=True,
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    """Command to cancel any current state."""
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(
            f'Нет активных комманд, чтобы их отменять {uchar.SHRUGGING}'
        )
        return
    await state.finish()
    await message.answer(
        f'Команда отменена {uchar.OK_HAND}',
        reply_markup=types.ReplyKeyboardRemove(),
    )
