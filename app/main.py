import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config import Config
from app.models import *
from app.utils.scheduler import Scheduler

bot = Bot(token=Config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


async def set_bot_commands(bot: Bot):
    logging.info('Configuring bot commands...')
    commands = [
        types.BotCommand('routes', 'список всех маршрутов'),
        types.BotCommand('routeadd', 'добавить маршрут'),
        types.BotCommand('help', 'помощь'),
        types.BotCommand('about', 'информация о боте'),
        types.BotCommand('settings', 'настройки'),
        types.BotCommand('cancel', 'отменить текущую команду')
    ]
    await bot.set_my_commands(commands)


async def on_startup(dp: Dispatcher):
    """
    Execute function before Bot start polling.
    """
    # initialize database and tables
    models = (
        User,
        Route,
        Schedule
    )
    db.create_tables(models)

    # start scheduler jobs
    Scheduler.start()

    # set bot commands for autocomplete
    await set_bot_commands(bot)


async def on_shutdown(dp: Dispatcher):
    """
    Execute function before Bot shut down polling.
    """
    # remove all jobs and shut down the Scheduler
    Scheduler.remove_all_jobs()
    Scheduler.shutdown()
