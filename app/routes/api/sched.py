from flask import Blueprint, current_app, jsonify, request
from datetime import datetime, timedelta

from app.scheduler.jobs import LottoCrawlerJob

bp = Blueprint("api/sched", __name__, url_prefix="/api/sched")

@bp.route("/")
@bp.route("/<path:cmd>")
def apiSchedCmd(cmd=None, job_id=None):
  launcher = current_app.config["launcher"]

  if cmd == "start":
    launcher.start()

  elif cmd == "stop":
    launcher.stop()

  elif cmd == "resume":
    launcher.resume()

  elif cmd == "pause":
    launcher.pause()

  return jsonify({
    "state": launcher.sched.state,
    "list": [ job.id for job in launcher.getJobs() ]
  }), 200


@bp.route("/job/list", methods=["GET"])
def apiSchedJobList():
  launcher = current_app.config["launcher"]
  
  return jsonify({
    "state": launcher.sched.state,
    "list": [ added_job.id for job in launcher.getJobs() ]
  }), 200


@bp.route("/job/state")
@bp.route("/job/state/<path:job_id>")
@bp.route("/job/state/<path:jobstore>/<path:job_id>")
def apiSchedJobState(job_id=None, jobstore=None):
  launcher = current_app.config["launcher"]
  
  state = launcher.getJobState(jobstore=jobstore, job_id=job_id)
  print( state )

  return jsonify({
    "state": launcher.sched.state,
    "list": state
  }), 200


@bp.route("/job/add", methods=["GET"])
def apiSchedJobAddView():
  launcher = current_app.config["launcher"]

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
  launcher = current_app.config["launcher"]
  
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
  
  added_job = launcher.addJob(job, args=["1", "2"], kwargs=data)

  return jsonify({
    "state": launcher.sched.state,
    "list": [ added_job.id for job in launcher.getJobs() ]
  }), 200


@bp.route("/job/remove")
@bp.route("/job/remove/<path:job_id>")
def apiSchedJobRemove(job_id=None):
  launcher = current_app.config["launcher"]
  
  if job_id is not None:
    if job_id == "all":
      launcher.removeAllJob()
    else:
      launcher.removeJob(job_id)

  return jsonify({
    "state": launcher.sched.state,
    "list": [ job.id for job in launcher.getJobs() ]
  }), 200
