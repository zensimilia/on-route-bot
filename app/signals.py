import logging

from playhouse.signals import post_delete, post_save

from app.models import Schedule
from app.utils.scheduler import Scheduler, add_job

log = logging.getLogger(__name__)

# TODO:
# [ ] add post_delete_route_handler with deletes cascade job schedules
# [ ] learn english more


def post_delete_schedule_handler(_, instance) -> None:
    """Callback function calls when schedule complete deleted."""
    Scheduler.remove_job(instance.id)


def post_save_schedule_handler(_, instance, created) -> None:
    """Callback function calls when schedule complete saved."""
    job = Scheduler.get_job(instance.id)
    if not job or created:
        add_job(instance)
        return
    if instance.is_active:
        job.resume()
    else:
        job.pause()


def register_signals():
    """Register signals for models."""
    log.info('Configuring signals for models...')
    post_delete.connect(post_delete_schedule_handler, sender=Schedule)
    post_save.connect(post_save_schedule_handler, sender=Schedule)
