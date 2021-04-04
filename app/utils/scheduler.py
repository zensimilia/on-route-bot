from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.config import Config
from app.models import Schedule, Route
import peewee
import logging
import json

log = logging.getLogger(__name__)

jobstores = {'default': SQLAlchemyJobStore(f'sqlite:///{Config.DB_FILE}')}

executors = {'default': AsyncIOExecutor()}

Scheduler = AsyncIOScheduler(
    jobstores=jobstores, executors=executors, timezone='Europe/Moscow'
)


# [x] берем все активные расписания
# [ ] перебираем их и добавляем job
# [ ] при изменении расписания, ищем его в jobs и обновляем/удаляем
# [ ] при добавлении расписания, добавляем его в jobs


def get_active_schedules() -> peewee.ModelSelect:
    """Returns all schedules with is_active property."""
    schedules: peewee.ModelSelect = (
        Route.select(Route, Schedule)
        .where(Route.is_active)
        .join(Schedule)
        .where(Schedule.is_active)
    )
    log.info('Found %s active schedules.', schedules.count())
    return schedules


async def test(route):
    from app.main import bot  # pylint: disable=import-outside-toplevel

    await bot.send_message(
        chat_id=route.user.uid, text=f'Test message. {route.schedule.id}'
    )
    # print(param)


def create_jobs(routes) -> None:
    for route in routes:
        # print(route.schedule)
        trigger = json.loads(route.schedule.schedule)
        _ = Scheduler.add_job(
            test,
            trigger=CronTrigger(
                hour=trigger['hour'],
                minute=trigger['minute'],
                day_of_week=trigger['day_of_week'],
            ),
            id=str(route.schedule),
            replace_existing=True,
            args=[route],
        )
