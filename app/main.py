import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config import Config
from app import models
from app.utils.scheduler import Scheduler, get_active_schedules, create_jobs

bot = Bot(token=Config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

log = logging.getLogger(__name__)


async def set_bot_commands(bot_instance: Bot):
    """Sets bot commands that can be selected from the list
    when user start typing a message from '/' symbol.

    Args:
        bot_instance (Bot): The Bot instance as is.
    """
    log.info('Configuring bot commands...')
    commands = [
        types.BotCommand('routes', 'список всех маршрутов'),
        types.BotCommand('routeadd', 'добавить маршрут'),
        types.BotCommand('help', 'помощь'),
        types.BotCommand('about', 'информация о боте'),
        types.BotCommand('settings', 'настройки'),
        types.BotCommand('cancel', 'отменить текущую команду'),
    ]
    await bot_instance.set_my_commands(commands)


async def on_startup(_: Dispatcher):
    """Execute function before Bot start polling."""
    # initialize database and tables
    models_list = (models.User, models.Route, models.Schedule)
    models.db.create_tables(models_list)

    # start scheduler jobs
    sched = get_active_schedules()
    create_jobs(sched)
    Scheduler.start()
    Scheduler.reschedule_job(
        '10', trigger='cron', minute='*/1', hour='*', day_of_week='*'
    )
    Scheduler.reschedule_job(
        '12', trigger='cron', minute='*/1', hour='*', day_of_week='*'
    )
    Scheduler.reschedule_job(
        '13', trigger='cron', minute='*/1', hour='*', day_of_week='*'
    )

    # set bot commands for autocomplete
    await set_bot_commands(bot)


async def on_shutdown(_: Dispatcher):
    """Execute function before Bot shut down polling."""
    # remove all jobs and shut down the Scheduler
    Scheduler.remove_all_jobs()
    Scheduler.shutdown()
