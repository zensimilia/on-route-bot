from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import utils.uchar as uchar
import models.db as db


async def cmd_start(message: types.Message):
    """
    Show welcome message and register user.

    :param obj message: Message object.
    """
    db.register_user(message.from_user.id, message.from_user.username)
    await message.answer('Welcome text!')


async def cmd_about(message: types.Message):
    """
    Show information about bot.
    """
    await message.answer("Hi! I'm the <b>Traffic Assistant Bot</b>. "
                         "\nI will warn you about traffic jams and weather forecast on your route by schedule. "
                         "\nI'am work yet with <a href='https://maps.yandex.com'>Yandex Maps</a> only.",
                         disable_web_page_preview=True)


async def cmd_cancel(message: types.Message, state: FSMContext):
    """
    Command to cancel any current state.
    """
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(f"Нет активной комманды которую нужно отменить {uchar.SHRUGGING}")
        return
    await state.finish()
    await message.answer(f"Команда отменена {uchar.OK_HAND}", reply_markup=types.ReplyKeyboardRemove())


async def something_went_wrong(messsage: types.Message, error: str = None):
    """
    Show error message when exception is raised.

    :param obj message: Message object.
    :param obj error: Error object with `__str__` method.
    """
    if error is None:
        error = 'Что-то пошло не так!'
    text = f'<b>{error}</b> \nПопробуйте позже или обратитесь к автору бота (ссылка в профиле).'
    await messsage.answer(text)


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_about, commands="about")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(
        cmd_cancel,
        Text(equals="отмена",
             ignore_case=True),
        state="*")
