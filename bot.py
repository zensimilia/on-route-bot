import os
import db
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

# Initialize environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Initialize database and tables
db.create_tables()


@dp.message_handler(commands=['about'])
async def send_about(message: types.Message):
    """
    This handler will be called when user sends `/about` command
    """
    await bot.send_message(message.chat.id, "Hi! I'm the <b>Traffic Assistant Bot</b>.\nI will warn you about traffic jams on your route by schedule.", parse_mode='html')


@dp.message_handler(commands=['register'])
async def register_user(message: types.Message):
    """
    This handler will be called when user sends `/register` command
    """
    user = db.register_user(message.from_user.id, message.from_user.username)

    print(user)

    if user:
        await bot.send_message(message.chat.id, "You was succefull registered!", parse_mode='html')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
