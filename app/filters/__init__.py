import logging

from aiogram.dispatcher.dispatcher import Dispatcher

from .is_name import IsName
from .is_url import IsUrl
from .is_time import IsTime


def register_filters(dp: Dispatcher):
    logging.info('Configuring filters...')
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
