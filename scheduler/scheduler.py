from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from scheduler.config import Config


class Scheduler:
    _instance = None

    def __new__(cls) -> BackgroundScheduler:
        if cls._instance is None:
            cls._instance = super(Scheduler, cls).__new__(cls)
            cls._scheduler = BackgroundScheduler(jobstores={"default": SQLAlchemyJobStore(url=Config.SQLALCHEMY_DATABASE_URI)})
            cls._scheduler.start()
        return cls._scheduler
