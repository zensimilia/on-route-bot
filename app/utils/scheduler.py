import json
import logging

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.job import Job
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import Config
from app.db import db_session
from app.models import Route, Schedule

log = logging.getLogger(__name__)

jobstores = {'default': SQLAlchemyJobStore(f'sqlite:///{Config.DB_FILE}')}
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
    with db_session() as db:
        schedules = (
            db.query(Schedule)
            .where((Schedule.is_active == True) & (Route.is_active == True))
            .join(Route)
        )
    log.info('Found %s active schedules.', schedules.count())
    print(schedules.all())  # need test
    return schedules


async def send_single_route(route):
    # REFACTOR ME PLS!!!
    from app.main import bot  # pylint: disable=import-outside-toplevel

    message = route.message()
    message = f'Уведомление по расписанию:\n{message}'

    await bot.send_message(chat_id=route.user.uid, text=message)


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
        args=[instance.route],
    )


def create_jobs(routes) -> None:
    for route in routes:
        add_job(route.schedules.first())
