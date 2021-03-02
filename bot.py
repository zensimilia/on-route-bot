import logging

from aiogram import executor

from app.config import Config
from app.handlers.common import register_handlers_common
from app.handlers.routes import register_handlers_routes
from app.handlers.settings import register_handlers_settings
from app.main import dp, on_startup

# configure logging
logging_level = logging.DEBUG if Config.DEBUG else logging.INFO
logging.basicConfig(level=logging_level)


def main():
    # register Dispatcher handlers
    register_handlers_common(dp)
    register_handlers_routes(dp)
    register_handlers_settings(dp)

    # start bot polling
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


if __name__ == '__main__':
    main()
