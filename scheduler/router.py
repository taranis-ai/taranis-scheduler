import uuid
from flask import Flask, render_template, Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_htmx import HTMX

from scheduler.scheduler import Scheduler
from scheduler.config import Config


def is_htmx_request() -> bool:
    return "HX-Request" in request.headers


class JobDetails(MethodView):
    @jwt_required(optional=Config.DEBUG)
    def get(self, job_id):
        job = Scheduler().get_job(job_id)
        if job:
            job_details = {
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time,
                "trigger": str(job.trigger),
                "args": job.args,
                "kwargs": job.kwargs,
            }
            return render_template("job_details_partial.html", job=job_details)

        return "Job not found", 404


class JobList(MethodView):
    @jwt_required(optional=Config.DEBUG)
    def get(self):
        search_term = request.args.get("search", "").lower()
        page = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 10))

        jobs = Scheduler().get_jobs()

        # Filter jobs by search term
        if search_term:
            jobs = [job for job in jobs if search_term in job.id.lower() or search_term in job.name.lower()]

        # Pagination logic
        total_jobs = len(jobs)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_jobs = jobs[start:end]

        if is_htmx_request():
            return render_template("jobs_partial.html", jobs=paginated_jobs, debug=Config.DEBUG)

        return render_template("index.html", jobs=paginated_jobs, page=page, total_jobs=total_jobs, page_size=page_size, debug=Config.DEBUG)

    @jwt_required(optional=Config.DEBUG)
    def post(self):
        if not Config.DEBUG:
            return jsonify({"error": "Job creation is disabled in production"}), 400
        job_name = request.form.get("name")
        job_interval: int = int(request.form.get("interval", 0))

        if job_name and job_interval > 0:
            job_id = str(uuid.uuid4())
            Scheduler().add_job(func=print, trigger="interval", seconds=job_interval, id=job_id, args=[f"Executing job {job_name}"])

            jobs = Scheduler().get_jobs()
            return render_template("jobs_partial.html", jobs=jobs, debug=Config.DEBUG)

        return jsonify({"error": "Invalid job data"}), 400

    @jwt_required(optional=Config.DEBUG)
    def delete(self):
        if not Config.DEBUG:
            return jsonify({"error": "Job deletion is disabled in production"}), 400
        job_id = request.args.get("job_id")

        if not job_id:
            return jsonify({"error": "Job ID not provided"}), 400

        Scheduler().remove_job(job_id)

        jobs = Scheduler().get_jobs()
        if is_htmx_request():
            return render_template("jobs_partial.html", jobs=jobs, debug=Config.DEBUG)

        return jsonify({"status": "success"})


def init(app: Flask):
    HTMX(app)

    jobs_bp = Blueprint("jobs", __name__, url_prefix=app.config["APPLICATION_ROOT"])

    jobs_bp.add_url_rule("/", view_func=JobList.as_view("jobindex"))
    jobs_bp.add_url_rule("/jobs", view_func=JobList.as_view("joblist"))
    jobs_bp.add_url_rule("/jobs/<job_id>", view_func=JobDetails.as_view("jobdetails"))

    app.register_blueprint(jobs_bp)
