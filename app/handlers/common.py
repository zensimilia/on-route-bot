from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import app.utils.uchar as uchar
from app.models import User
from app.main import bot

from app.utils.scheduler import scheduler
from apscheduler.triggers.cron import CronTrigger


async def cmd_start(message: types.Message):
    """
    Show welcome message and register user.

    :param obj message: Message object.
    """
    User.create(uid=message.from_user.id, username=message.from_user.username)
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
        await message.answer(f"Нет активных комманд, чтобы их отменять {uchar.SHRUGGING}")
        return
    await state.finish()
    await message.answer(f"Команда отменена {uchar.OK_HAND}", reply_markup=types.ReplyKeyboardRemove())


async def schedule_test(message: types.Message):
    scheduler.add_job(say_hello, trigger=CronTrigger(
        minute='*/1'), id="job", kwargs={'chat': message.chat.id})
    await message.answer('Test is run...')


async def say_hello(chat: int):
    import datetime
    await bot.send_message(chat_id=chat, text=f"Hello! Current time is: {datetime.datetime.now()}")


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(schedule_test, commands="test")
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(cmd_about, commands="about")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(
        cmd_cancel,
        Text(equals="отмена",
             ignore_case=True),
        state="*")


# @dp.message_handler(commands=['tz'])
# async def get_user_location(message: types.Message):
#     """
#     Set timezone for user.
#     """
#     keyboard = types.ReplyKeyboardMarkup(
#         row_width=1, resize_keyboard=True)
#     button_geo = types.KeyboardButton(
#         text="Отправить местоположение",
#         request_location=True)
#     keyboard.add(button_geo)
#     await message.answer("Отправьте своё местоположение для определения часового пояса или введите вручную.\n"
#                          "Например: <code>UTC+3</code> или <code>Europe/Moscow</code>.", reply_markup=keyboard)


# # @dp.message_handler(content_types=['location'])
# async def set_user_timezone(message: types.Message):
#     if message.location:
#         url = "http://api.geonames.org/timezoneJSON?formatted=true&lat={}&lng={}&username={}".format(
#             message.location.latitude, message.location.longitude, Config.GEONAMES_USER)
#         r = requests.get(url)
#         timezone = r.json()['timezoneId']
#         db.add_user_timezone(message.from_user.id, timezone)
#         await bot.send_message(message.chat.id, f'Ваш часовой пояс (timezone): <code>{timezone}</code> успешно сохранён.', reply_markup=types.ReplyKeyboardRemove())
#     else:
#         await bot.send_message(message.chat.id, 'Cant get location.', reply_markup=types.ReplyKeyboardRemove())


# # @dp.message_handler(Text(startswith=['utc'], ignore_case=True))
# async def set_timezone_by_utc(message: types.Message):
#     """
#     Set user timezone in UTC format.
#     """
#     timezone = message.text.upper().split(' ')[0]
#     db.add_user_timezone(message.from_user.id, timezone)
#     await message.answer(f'Ваш часовой пояс установлен как <code>{timezone}</code>', reply_markup=types.ReplyKeyboardRemove())
