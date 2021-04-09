import datetime
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from apscheduler.triggers.cron import CronTrigger

from app.main import bot
from app.models import User
from app.utils import uchar
from app.utils.scheduler import Scheduler
from app.db import db_session

log = logging.getLogger(__name__)


async def cmd_start(message: types.Message):
    """Show welcome message and register user.

    :param obj message: Message object.
    """
    with db_session() as db:
        user = User(
            uid=message.from_user.id, username=message.from_user.username
        )
        db.add(user)
    await message.answer('Welcome text!')


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


async def schedule_test(message: types.Message):
    Scheduler.add_job(
        say_hello,
        trigger=CronTrigger(minute='*/1'),
        id='job',
        kwargs={'chat': message.chat.id},
    )
    message_date = message.date
    await message.answer(f'Message date: {message_date}')


async def say_hello(chat: int):
    await bot.send_message(
        chat_id=chat, text=f'Hello! Current time is: {datetime.datetime.now()}'
    )
