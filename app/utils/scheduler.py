import json
import logging
from typing import Optional

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.job import Job
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.db import db_engine, db_session
from app.models import Route, Schedule

log = logging.getLogger(__name__)

jobstores = {'default': SQLAlchemyJobStore(engine=db_engine)}
jobdefaults = {'misfire_grace_time': 30, 'coalesce': True}
executors = {'default': AsyncIOExecutor()}

Scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    executors=executors,
    timezone='Europe/Moscow',
    job_defaults=jobdefaults,
)


def get_active_schedules():
    """Returns all schedules with is_active property."""
    schedules = Schedule.get_active()
    log.info('Found %s active schedules.', len(schedules))
    return schedules


async def send_single_route(route_id: int):
    # REFACTOR ME PLS!!!
    from app.main import bot  # pylint: disable=import-outside-toplevel

    with db_session() as db:
        route = db.get(Route, route_id)
        uid = route.user.uid
    message = route.message()
    message = f'Уведомление по расписанию:\n{message}'

    await bot.send_message(chat_id=uid, text=message)


def add_job(instance) -> Job:
    trigger = json.loads(instance.cron)

    return Scheduler.add_job(
        send_single_route,
        trigger=CronTrigger(
            hour=trigger['hour'],
            minute=trigger['minute'],
            day_of_week=trigger['day_of_week'],
        ),
        id=str(instance.id),
        replace_existing=True,
        args=[instance.route_id],
    )


def remove_job(job_id: int, jobstore: Optional[str] = None) -> None:
    try:
        Scheduler.remove_job(job_id, jobstore=jobstore)
    except JobLookupError as e:
        log.info('%s - Nothing to remove.', e)
        pass


def create_jobs(schedules) -> None:
    for schedule in schedules:
        add_job(schedule)
