from flask import Flask
from scheduler import router, scheduler, auth
from scheduler.config import Config
from scheduler.jobs import Jobs


def create_app():
    app = Flask(__name__, static_url_path=f"{Config.APPLICATION_ROOT}/static")
    app.config.from_object("scheduler.config.Config")

    with app.app_context():
        init(app)

    return app


def init(app: Flask):
    auth.init(app)
    scheduler.Scheduler()
    router.init(app)
    if app.config.get("DEBUG"):
        Jobs.schedule_debug_job()
