from aiogram import executor

from app.config import Config
from app.handlers.common import register_handlers_common
from app.handlers import (register_handlers_routes, register_handlers_schedules,
                          register_handlers_settings, register_errors_handler)
from app.main import dp, on_startup, on_shutdown
from app.filters import register_filters
from app.utils.log import configure_logging


def main():
    # register custom filters
    register_filters(dp)

    # configure logging
    configure_logging(Config.LOG_CONFIG)

    # register Dispatcher handlers
    register_handlers_common(dp)
    register_handlers_routes(dp)
    register_handlers_schedules(dp)
    register_handlers_settings(dp)
    register_errors_handler(dp)

    # start bot polling
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
