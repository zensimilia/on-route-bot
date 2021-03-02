import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.models import *
from app.config import Config
from app.handlers.common import register_handlers_common
from app.handlers.routes import register_handlers_routes
from app.handlers.settings import register_handlers_settings

from app.utils.scheduler import scheduler


# configure logging
logging_level = logging.DEBUG if Config.DEBUG else logging.INFO
logging.basicConfig(level=logging_level)

# initialize bot and dispatcher
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


def main():
    # register Dispatcher handlers
    register_handlers_common(dp)
    register_handlers_routes(dp)
    register_handlers_settings(dp)

    # start bot polling
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
