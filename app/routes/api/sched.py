from flask import Blueprint, current_app, jsonify, request
from datetime import datetime, timedelta

from app.scheduler.jobs import LottoCrawlerJob

bp = Blueprint("api/sched", __name__, url_prefix="/api/sched")

@bp.route("/")
@bp.route("/<path:cmd>")
def apiSchedCmd(cmd=None, job_id=None):
  scheduler = current_app.config["scheduler"]

  if cmd == "start":
    scheduler.start()

  elif cmd == "stop":
    scheduler.stop()

  elif cmd == "resume":
    scheduler.resume()

  elif cmd == "pause":
    scheduler.pause()

  return jsonify({
    "state": scheduler.sched.state,
    "list": [ job.id for job in scheduler.getJobs() ]
  }), 200


@bp.route("/job/list", methods=["GET"])
def apiSchedJobList():
  scheduler = current_app.config["scheduler"]
  
  return jsonify({
    "state": scheduler.sched.state,
    "list": [ added_job.id for job in scheduler.getJobs() ]
  }), 200


@bp.route("/job/state")
@bp.route("/job/state/<path:job_id>")
@bp.route("/job/state/<path:jobstore>/<path:job_id>")
def apiSchedJobState(job_id=None, jobstore=None):
  scheduler = current_app.config["scheduler"]
  
  state = scheduler.getJobState(jobstore=jobstore, job_id=job_id)
  print( state )

  return jsonify({
    "state": scheduler.sched.state,
    "list": state
  }), 200


@bp.route("/job/add", methods=["GET"])
def apiSchedJobAddView():
  scheduler = current_app.config["scheduler"]

  return '''
  <form action="/api/sched/job/add" method="POST">
    <input name="job_id" placeholder="Job ID">
    <input name="schedule_type" placeholder="Schedule Type">
    <input name="seconds" placeholder="seconds">
    <button type="submit">Submit</button>
  </form>
  '''


@bp.route("/job/add", methods=["POST"])
@bp.route("/job/add/<path:jobsotre>", methods=["POST"])
def apiSchedJobAdd(jobsotre=None):
  scheduler = current_app.config["scheduler"]
  
  method = request.method
  data = None
  if method == "GET":
    data = dict(request.args) # ImmutableMultiDict -> Dict
  elif method == "POST":
    data = dict(request.json if request.json is not None else request.form)

  if data is None:
    pass

  job_id = data.get("job_id", None)

  # TODO: Dynamical allocate
  job = LottoCrawlerJob(
    name=job_id,
    scheduled_type="date",
    run_date=datetime.now()+timedelta(seconds=10)
  )
  
  added_job = scheduler.addJob(job, args=["1", "2"], kwargs=data)

  return jsonify({
    "state": scheduler.sched.state,
    "list": [ added_job.id for job in scheduler.getJobs() ]
  }), 200


@bp.route("/job/remove")
@bp.route("/job/remove/<path:job_id>")
def apiSchedJobRemove(job_id=None):
  scheduler = current_app.config["scheduler"]
  
  if job_id is not None:
    if job_id == "all":
      scheduler.removeAllJob()
    else:
      scheduler.removeJob(job_id)

  return jsonify({
    "state": scheduler.sched.state,
    "list": [ job.id for job in scheduler.getJobs() ]
  }), 200