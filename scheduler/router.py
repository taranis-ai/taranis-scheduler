import uuid
from flask import Flask, render_template, Blueprint, request, jsonify
from flask.views import MethodView
from flask_htmx import HTMX
from scheduler.filters import human_readable_trigger

from scheduler.core_api import CoreApi
from scheduler.config import Config


def is_htmx_request() -> bool:
    return "HX-Request" in request.headers


class JobDetails(MethodView):
    def get(self, job_id: str):
        if job := CoreApi().get_schedule_by_id(job_id):
            return render_template("job_details_partial.html", job=job, debug=Config.DEBUG)

        return "Job not found", 404


class JobList(MethodView):
    def get(self):
        search_term = request.args.get("search", "").lower()
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 10))

        result = CoreApi().get_schedule({"page": page, "page_size": page_size, "search": search_term})

        if result is None:
            return f"Failed to fetch jobs from: {Config.TARANIS_CORE_URL}", 500

        if is_htmx_request():
            return render_template("jobs_partial.html", jobs=result["items"], debug=Config.DEBUG)

        return render_template(
            "index.html", jobs=result["items"], page=page, total_jobs=result["total_count"], page_size=page_size, debug=Config.DEBUG
        )

    def post(self):
        if not Config.DEBUG:
            return jsonify({"error": "Job creation is disabled in production"}), 400
        job_name = request.form.get("name")
        job_interval: int = int(request.form.get("interval", 0))

        if job_name and job_interval > 0:
            job_id = str(uuid.uuid4())
            CoreApi().add_schedule({"func": "print", "trigger": "interval", "seconds": "job_interval", "id": job_id, "args": "debug job"})

            jobs = CoreApi().get_schedule()
            return render_template("jobs_partial.html", jobs=jobs, debug=Config.DEBUG)

        return jsonify({"error": "Invalid job data"}), 400

    def delete(self):
        if not Config.DEBUG:
            return jsonify({"error": "Job deletion is disabled in production"}), 400
        job_id = request.args.get("job_id")

        if not job_id:
            return jsonify({"error": "Job ID not provided"}), 400

        CoreApi().delete_schedule(job_id)

        jobs = CoreApi().get_schedule()
        if is_htmx_request():
            return render_template("jobs_partial.html", jobs=jobs, debug=Config.DEBUG)

        return jsonify({"status": "success"})


def init(app: Flask):
    HTMX(app)
    app.jinja_env.filters["human_readable"] = human_readable_trigger

    jobs_bp = Blueprint("jobs", __name__, url_prefix=app.config["APPLICATION_ROOT"])

    jobs_bp.add_url_rule("/", view_func=JobList.as_view("jobindex"))
    jobs_bp.add_url_rule("/jobs", view_func=JobList.as_view("joblist"))
    jobs_bp.add_url_rule("/jobs/<string:job_id>", view_func=JobDetails.as_view("jobdetails"))

    app.register_blueprint(jobs_bp)
