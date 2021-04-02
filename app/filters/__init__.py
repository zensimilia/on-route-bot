import logging

from aiogram.dispatcher.dispatcher import Dispatcher

from .is_name import IsName
from .is_time import IsTime
from .is_url import IsUrl

log = logging.getLogger(__name__)


def register_filters(dp: Dispatcher):
    log.info('Configuring filters...')
    text_messages = [
        dp.message_handlers,
        dp.edited_message_handlers,
        dp.channel_post_handlers,
        dp.edited_channel_post_handlers,
    ]
    dp.filters_factory.bind(IsName,
                            event_handlers=text_messages)
    dp.filters_factory.bind(IsUrl,
                            event_handlers=text_messages)
    dp.filters_factory.bind(IsTime,
                            event_handlers=text_messages)
