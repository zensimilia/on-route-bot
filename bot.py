import db
import time
import logging
import requests
from config import Config
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types

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
    # headers = {'User-Agent': 'Mozilla/5.0'}
    # response = requests.get(url, headers=headers)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup.get_text())
    # logging.debug(soup.find('div', class_='_mfyskr'))
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


@dp.message_handler(commands=['location'])
async def get_user_location(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(
        text="Отправить местоположение",
        request_location=True,
        callback_data=message)
    keyboard.add(button_geo)
    await message.answer("Отправьте местоположение для определения часового пояса или введите вручную (например: <code>UTC+3</code> или <code>Europe/Moscow</code>).", reply_markup=keyboard)


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


@dp.message_handler(commands=['map'])
async def send_map_image(message: types.Message):
    timestamp = time.ctime()
    url = f'https://static-maps.yandex.ru/1.x/?l=map,trf&size=650,450&bbox=38.973102,45.021841~38.903821,45.075021&={timestamp}'
    await message.answer_photo(url, caption='MAP')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
