import logging

from aiogram.dispatcher.dispatcher import Dispatcher

from .is_name import IsNameFilter
from .is_url import IsUrlFilter

log = logging.getLogger(__name__)


def register_filters(dp: Dispatcher):
    log.info('Configuring filters...')
    text_messages = [
        dp.message_handlers,
        dp.edited_message_handlers,
        dp.channel_post_handlers,
        dp.edited_channel_post_handlers,
    ]
    dp.filters_factory.bind(IsNameFilter, event_handlers=text_messages)
    dp.filters_factory.bind(IsUrlFilter, event_handlers=text_messages)
