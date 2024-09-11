from datetime import datetime
from scheduler import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from celery import Celery

from scheduler.config import Config


class Jobs:
    sched: BackgroundScheduler = scheduler.Scheduler()
    celery: Celery = Celery("taranis-ai")
    celery.config_from_object(Config.CELERY)
    celery.set_default()

    @classmethod
    def schedule_debug_job(cls):
        if not Jobs.sched.get_job("Test"):
            try:
                Jobs.sched.add_job(func=cls.debug_job, trigger="interval", seconds=30, id="Test", max_instances=1)
            except Exception as e:
                print(e)

    @classmethod
    def debug_job(cls):
        print(f"Debug job executed - {datetime.now()} - {scheduler.Scheduler().get_jobs()}")


def send_celery_task(task, args=None, queue="misc", task_id=None):
    Jobs.celery.send_task(task, args=args, queue=queue, task_id=task_id)
