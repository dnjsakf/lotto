from flask import (
  Blueprint,
  render_template,
  jsonify,
  request
)
from app.models.oracle import (
  JobListModel,
  JobSchedListModel,
  JobSchedDateListModel
)

bp = Blueprint("job", __name__, url_prefix="/job")

@bp.route("/list", methods=["GET"])
def view_job_list():
  model = JobSchedListModel()
  datas = model.getDatas()

  return render_template(
    "/views/sched/list.jinja",
    datas=datas,
    pageInfo=model.Meta.page_info
  )

@bp.route("/write", methods=["GET","POST"])
@bp.route("/write/<path:sch_id>", methods=["GET","POST"])
def view_job_write(sch_id=None):
  method = request.method

  if method == "GET":
    jobListModel = JobListModel()
    model = JobSchedListModel(schId=sch_id)
    data = model.dump()

    return render_template(
      "/views/sched/write.jinja",
      datas=data,
      job_options=jobListModel.getDatas()
    )

  elif method == "POST":
    data = dict(request.form)
    schType = data.get("schType", None)

    temp = JobSchedListModel()
    print( temp.dump() )
    
    model = JobSchedListModel(data)
    print( model.dump() )
    update_count = model.insert()

    if schType == "date":
      model = JobSchedDateListModel(data, schId=model.get("schId"))
      update_count = model.insert(commit=True) # commiter
    
    elif schType == "interval":
      pass
      
    elif schType == "cron":
      pass

    return jsonify({
      "success": bool(update_count)
    })

  return render_template("/views/sched/write.jinja")