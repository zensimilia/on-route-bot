import logging
from .routes import *
from .schedules import *
from aiogram.dispatcher import Dispatcher


def register_handlers_routes(dp: Dispatcher):
    """
    Register routes handlers in Dispatcher.
    """
    logging.info('Configuring routes handlers...')
    dp.register_message_handler(
        route_list,
        commands='routes')
    dp.register_message_handler(
        route_add,
        commands='routeadd')
    dp.register_message_handler(
        route_add_name,
        is_name=True,
        state=CreateRoute.name)
    dp.register_message_handler(
        route_add_url,
        is_url=True,
        state=CreateRoute.url)
    dp.register_message_handler(
        route_add_error,
        is_url=False,
        state=CreateRoute)
    dp.register_message_handler(
        route_add_error,
        is_name=False,
        state=CreateRoute)
    dp.register_callback_query_handler(
        route_list,
        cd_routes.filter(action='list')
    )
    dp.register_callback_query_handler(
        route_select,
        cd_routes.filter(action='select')
    )
    dp.register_callback_query_handler(
        route_select,
        cd_routes.filter(action='toggle')
    )
    dp.register_callback_query_handler(
        route_show,
        cd_routes.filter(action='show')
    )
    dp.register_callback_query_handler(
        route_delete,
        cd_routes.filter(action='delete')
    )
    dp.register_callback_query_handler(
        route_select,
        cd_routes.filter(action='delete_no')
    )
    dp.register_callback_query_handler(
        route_delete_confirm,
        cd_routes.filter(action='delete_confirm')
    )


def register_handlers_schedules(dp: Dispatcher):
    """
    Register schedule handlers in Dispatcher.
    """
    logging.info('Configuring schedule handlers...')
    dp.register_message_handler(
        schedule_add_time,
        is_time=True,
        state=CreateSchedule.time)
    dp.register_callback_query_handler(
        schedule_add_days,
        cd_schedule_days.filter(),
        state=CreateSchedule.days)
    dp.register_message_handler(
        schedule_add_error,
        is_time=False,
        state=CreateSchedule
    )
