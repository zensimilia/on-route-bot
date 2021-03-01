from apscheduler.executors.asyncio import AsyncIOExecutor
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

jobstores = {
    'default': MemoryJobStore()
}

executors = {
    'default': AsyncIOExecutor()
}

scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors)
