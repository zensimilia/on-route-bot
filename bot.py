import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import app.models
from app.config import Config
from app.handlers.common import register_handlers_common
from app.handlers.routes import register_handlers_routes

# configure logging
logging_level = logging.DEBUG if Config.DEBUG else logging.INFO
logging.basicConfig(level=logging_level)

# initialize bot and dispatcher
bot = Bot(token=Config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


def main():
    # registration handlers
    register_handlers_common(dp)
    register_handlers_routes(dp)

    # initialize database and tables
    models = (
        app.models.User,
        app.models.Route
    )
    app.models.db.create_tables(models)

    # start bot polling
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
