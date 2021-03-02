from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config import Config
from app.models import *
from app.utils.scheduler import scheduler

bot = Bot(token=Config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


async def set_bot_commands(bot: Bot):
    commands = [
        types.BotCommand('routes', 'список всех маршрутов'),
        types.BotCommand('routeadd', 'добавить маршрут'),
        types.BotCommand('about', 'информация о боте'),
        types.BotCommand('cancel', 'отменить текущую команду')
    ]
    await bot.set_my_commands(commands)


async def on_startup(dispatcher: Dispatcher):
    # initialize database and tables
    models = (
        User,
        Route
    )
    db.create_tables(models)

    # start scheduler jobs
    scheduler.start()

    # set bot commands for autocomplete
    await set_bot_commands(bot)
