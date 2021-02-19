import logging

import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

import models.db as db  # database model
import keyboards.common as keyboards  # chat keyboards
from config import Config
from handlers.common import register_handlers_common
from handlers.routes import register_handlers_routes

# configure constants from environment
BOT_TOKEN = Config.BOT_TOKEN
GEONAMES_USER = Config.GEONAMES_USER

# configure logging
logging_level = logging.DEBUG if Config.DEBUG else logging.INFO
logging.basicConfig(level=logging_level)

# initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# registration handlers
register_handlers_common(dp)
register_handlers_routes(dp)

# initialize database and tables
db.create_tables()


@dp.message_handler(commands=['tz'])
async def get_user_location(message: types.Message):
    """
    Set timezone for user.
    """
    keyboard = types.ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(
        text="Отправить местоположение",
        request_location=True)
    keyboard.add(button_geo)
    await message.answer("Отправьте своё местоположение для определения часового пояса или введите вручную.\n"
                         "Например: <code>UTC+3</code> или <code>Europe/Moscow</code>.", reply_markup=keyboard)


@dp.message_handler(content_types=['location'])
async def set_user_timezone(message: types.Message):
    if message.location:
        url = "http://api.geonames.org/timezoneJSON?formatted=true&lat={}&lng={}&username={}".format(
            message.location.latitude, message.location.longitude, GEONAMES_USER)
        r = requests.get(url)
        timezone = r.json()['timezoneId']
        db.add_user_timezone(message.from_user.id, timezone)
        await bot.send_message(message.chat.id, f'Ваш часовой пояс (timezone): <code>{timezone}</code> успешно сохранён.', reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, 'Cant get location.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(startswith=['utc'], ignore_case=True))
async def set_timezone_by_utc(message: types.Message):
    """
    Set user timezone in UTC format.
    """
    timezone = message.text.upper().split(' ')[0]
    db.add_user_timezone(message.from_user.id, timezone)
    await message.answer(f'Ваш часовой пояс установлен как <code>{timezone}</code>', reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
