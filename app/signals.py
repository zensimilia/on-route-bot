import logging

from sqlalchemy import event

from app.models import Schedule
from app.utils.scheduler import Scheduler, add_job

log = logging.getLogger(__name__)

# TODO:
# [ ] add post_delete_route_handler with deletes cascade job schedules
# [x] learn english more


def register_signals() -> None:
    """Register signals for models."""
    log.info('Registering signals for models...')
    event.listen(Schedule, 'after_delete', cb_after_delete_schedule)
    event.listen(Schedule, 'after_insert', cb_after_insert_schedule)
    event.listen(Schedule, 'after_update', cb_after_update_schedule)


def cb_after_delete_schedule(mapper, connection, target) -> None:
    """Callback function calls when schedule event delete is triggered."""
    Scheduler.remove_job(target.id)


def cb_after_insert_schedule(mapper, connection, target) -> None:
    """Callback function calls when schedule event insert is triggered."""
    add_job(target)


def cb_after_update_schedule(mapper, connection, target) -> None:
    """Callback function calls when schedule event update is triggered."""
    if target.is_active is True:
        add_job(target)
    else:
        Scheduler.remove_job(target.id)
