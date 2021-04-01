import logging
from . import routes, errors, schedules, settings
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from app.states import CreateRoute, CreateSchedule, SetTimezone
from app.keyboards.inline_route import cd_routes
from app.keyboards.settings import cd_settings
from app.keyboards.inline_schedule import cd_schedules, cd_schedule_days


log = logging.getLogger(__name__)


def register_errors_handler(dp: Dispatcher):
    """Register handler for errors."""
    log.info('Configuring errors handlers...')
    dp.register_errors_handler(errors.errors_handler)


def register_handlers_routes(dp: Dispatcher):
    """Register routes handlers in Dispatcher."""
    log.info('Configuring routes handlers...')
    dp.register_message_handler(
        routes.route_list,
        commands='routes'
    )
    dp.register_message_handler(
        routes.route_add,
        commands='routeadd'
    )
    dp.register_message_handler(
        routes.route_add_name,
        is_name=True,
        state=CreateRoute.name
    )
    dp.register_message_handler(
        routes.route_add_url,
        is_url=True,
        state=CreateRoute.url
    )
    dp.register_message_handler(
        routes.route_add_error,
        is_url=False,
        state=CreateRoute
    )
    dp.register_message_handler(
        routes.route_add_error,
        is_name=False,
        state=CreateRoute
    )
    dp.register_callback_query_handler(
        routes.route_list,
        cd_routes.filter(action='list')
    )
    dp.register_callback_query_handler(
        routes.route_select,
        cd_routes.filter(action='select')
    )
    dp.register_callback_query_handler(
        routes.route_select,
        cd_routes.filter(action='toggle')
    )
    dp.register_callback_query_handler(
        routes.route_show,
        cd_routes.filter(action='show')
    )
    dp.register_callback_query_handler(
        routes.route_delete,
        cd_routes.filter(action='delete')
    )
    dp.register_callback_query_handler(
        routes.route_select,
        cd_routes.filter(action='delete_no')
    )
    dp.register_callback_query_handler(
        routes.route_delete_confirm,
        cd_routes.filter(action='delete_confirm')
    )


def register_handlers_schedules(dp: Dispatcher):
    """Register schedule handlers in Dispatcher."""
    log.info('Configuring schedule handlers...')
    dp.register_message_handler(
        schedules.schedule_add_time,
        is_time=True,
        state=CreateSchedule.time
    )
    dp.register_callback_query_handler(
        schedules.schedule_add_days,
        cd_schedule_days.filter(),
        state=CreateSchedule.days
    )
    dp.register_message_handler(
        schedules.schedule_add_error,
        is_time=False,
        state=CreateSchedule
    )
    dp.register_callback_query_handler(
        schedules.schedule_list,
        cd_routes.filter(action='schedule')
    )
    dp.register_callback_query_handler(
        schedules.schedule_add,
        cd_schedules.filter(action='add')
    )


def register_handlers_settings(dp: Dispatcher):
    """Register routes handlers in Dispatcher."""
    log.info('Configuring settings handlers...')
    dp.register_message_handler(settings.settings_list, commands='settings')
    dp.register_callback_query_handler(
        settings.settings_list,
        cd_settings.filter(action='list')
    )
    dp.register_callback_query_handler(
        settings.settings_tz,
        cd_settings.filter(action='tz')
    )
    dp.register_callback_query_handler(
        settings.settings_tz_change,
        cd_settings.filter(action='tz-change')
    )
    dp.register_message_handler(
        settings.settings_tz_set,
        Text(
            startswith='UTC',
            ignore_case=True
        ),
        state=SetTimezone
    )
    dp.register_message_handler(settings.settings_tz_error, state=SetTimezone)
