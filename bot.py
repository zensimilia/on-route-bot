import logging
import time
from aiogram.types.inline_keyboard import InlineKeyboardMarkup

import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

import db
import uchar  # unicode characters and emoji
import keyboards
from config import Config
from mod.parser import YAMParser, YAParseError, YARequestError, YAWParser

# Configure constants from environment
BOT_TOKEN = Config.BOT_TOKEN
GEONAMES_USER = Config.GEONAMES_USER

# Configure logging
logging_level = logging.DEBUG if Config.DEBUG else logging.INFO
logging.basicConfig(level=logging_level)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Initialize database and tables
db.create_tables()


@dp.message_handler(commands=['about'])
async def send_about(message: types.Message):
    """
    This handler will be called when user sends `/about` command
    """
    await message.answer("Hi! I'm the <b>Traffic Assistant Bot</b>.\nI will warn you about traffic jams on your route by schedule.")


@dp.message_handler(commands=['register'])
async def register_user(message: types.Message):
    """
    This handler will be called when user sends `/register` command
    """
    user = db.register_user(message.from_user.id, message.from_user.username)

    if user:
        await message.answer("You was succefull registered!")


@dp.message_handler(commands=['routeadd'])
async def add_route(message: types.Message):
    """
    This handler will be called when user sends `/route` command
    """
    db.register_user(message.from_user.id, message.from_user.username)
    url, *name = message.get_args().split()
    route = db.add_route(message.from_user.id, url, (name or ('',))[0])
    bot_answer = "Маршрут добавлен." if route else "Что-то пошло не так!"
    await message.answer(bot_answer)


@dp.message_handler(commands=['routes'])
async def all_routes(message: types.Message):
    """
    Display all user routes.
    """
    data = db.get_routes(message.from_user.id)
    for idx, route in enumerate(data, start=1):
        bot_answer = f'{idx} route url: {route[2]}'
        await message.answer(bot_answer, disable_web_page_preview=True)


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
        await bot.send_message(message.chat.id, f'Your location: {timezone}', reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, 'Cant get location.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(Text(startswith=['utc'], ignore_case=True))
async def set_timezone_by_utc(message: types.Message):
    """
    Set user timezone as UTC format.
    """
    timezone = message.text.upper().split(' ')[0]
    db.add_user_timezone(message.from_user.id, timezone)
    await message.answer(f'Ваш часовой пояс установлен как <code>{timezone}</code>', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['map'])
async def send_map_image(message: types.Message):
    await bot.send_chat_action(message.from_user.id, action=types.ChatActions.TYPING)
    timestamp = time.ctime()
    try:
        yamp = YAMParser('https://yandex.ru/maps/-/CCUMf0bhoD')
        map_center = yamp.coords
        yawp = YAWParser(map_center['lat'], map_center['lon'])
        temp = yawp.temp + f' {uchar.DEGREE}C'
        fact = yawp.fact + '.'
        map_url = f'{yamp.map}&={timestamp}'
        inline_buttons = keyboards.route_buttons(
            123, route_url=yamp.url, weather_url=yawp.url)
        await message.answer_photo(map_url, caption=f'Время в пути: <b>{yamp.time}</b>.\nПрогноз погоды: <b>{temp}</b> {fact}\n', reply_markup=inline_buttons)
    except (YAParseError, YARequestError) as e:
        await message.answer(e)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('route_edit_'))
async def process_callback_route_edit(callback_query: types.CallbackQuery):
    route_id = callback_query.data.split('_')[-1]
    # await bot.answer_callback_query(
    #     callback_query.id,
    #     text=f'route_id: {route_id}', show_alert=True)
    # await bot.answer_callback_query(callback_query.id)
    # await bot.send_message(callback_query.from_user.id, f'Редактировать маршрут {route_id}')
    # await callback_query.answer(f'Редактировать маршрут {route_id}')
    inline_buttons = keyboards.route_edit_buttons(123)
    await bot.send_message(callback_query.from_user.id, f'Редактировать маршрут {route_id}', reply_markup=inline_buttons)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
