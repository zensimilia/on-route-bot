import logging
from aiogram.types import Update

log = logging.getLogger(__name__)


async def errors_handler(update: Update, exception: Exception) -> bool:
    """ Exceptions handler. Catches all exceptions within task factory tasks.
    :param update: Object of incoming update.
    :param exception: An exception object.
    """
    # todo:
    # [ ] implement DM or email with traceback to admin
    # [ ] set logger name as function/module where exception is occur

    log.exception(exception)
    return True
