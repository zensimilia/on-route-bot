import logging

from sqlalchemy import event

from app.models import Route, Schedule
from app.utils import scheduler

log = logging.getLogger(__name__)


def register_signals() -> None:
    """Register signals for models."""
    log.info('Configuring signals for models...')
    event.listen(Schedule, 'after_delete', cb_after_delete_schedule)
    event.listen(Schedule, 'after_insert', cb_after_insert_schedule)
    event.listen(Schedule, 'after_update', cb_after_update_schedule)
    event.listen(Route, 'before_delete', cb_before_delete_route)
    event.listen(Route, 'after_update', cb_after_update_route)


def cb_after_delete_schedule(mapper, connection, target) -> None:
    """Callback function calls after schedule delete event is triggered."""
    scheduler.remove_job(target.id)


def cb_after_insert_schedule(mapper, connection, target) -> None:
    """Callback function calls after schedule insert event is triggered."""
    if target.route.is_active is True:
        scheduler.add_job(target)


def cb_after_update_schedule(mapper, connection, target) -> None:
    """Callback function calls after schedule update event is triggered."""
    if target.is_active is True and target.route.is_active is True:
        scheduler.add_job(target)
    else:
        scheduler.remove_job(target.id)


def cb_before_delete_route(mapper, connection, target) -> None:
    """Callback function calls before route delete event is triggered."""
    for schedule in target.schedules:
        scheduler.remove_job(schedule.id)


def cb_after_update_route(mapper, connection, target) -> None:
    """Callback function calls after route update event is triggered."""
    for schedule in target.schedules:
        if target.is_active is True and schedule.is_active is True:
            scheduler.add_job(schedule)
        else:
            scheduler.remove_job(schedule.id)
