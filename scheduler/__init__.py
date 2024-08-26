from flask import Flask
from scheduler import router, scheduler, auth


def create_app():
    app = Flask(__name__)
    app.config.from_object("scheduler.config.Config")

    with app.app_context():
        init(app)

    return app


def init(app: Flask):
    auth.init(app)
    scheduler.Scheduler()
    router.init(app)
    try:
        scheduler.Scheduler().add_job(func=print, trigger="interval", seconds=10, id="Test", max_instances=1, args=["Executing job"])
    except Exception as e:
        print(e)
