from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import Config

jobstores = {
    'default': SQLAlchemyJobStore(f'sqlite:///{Config.DB_FILE}')
}

executors = {
    'default': AsyncIOExecutor()
}

scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors)
