from aiogram.dispatcher.dispatcher import Dispatcher
from .is_route_valid import IsRouteVaildFilter
import logging


def register_filters(dp: Dispatcher):
    logging.info('Configuring filters...')
    text_messages = [
        dp.message_handlers,
        dp.edited_message_handlers,
        dp.channel_post_handlers,
        dp.edited_channel_post_handlers,
    ]
    # dp.filters_factory.bind(IsRouteVaildFilter, event_handlers=text_messages)
    dp.bind_filter(IsRouteVaildFilter)
