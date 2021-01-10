from flask import (
  Blueprint,
  render_template,
  jsonify,
  request
)
from app.models.oracle import LottoApiListModel, LottoJobListModel

bp = Blueprint("lotto", __name__, url_prefix="/lotto")

@bp.route("/list", methods=["GET", "POST"])
@bp.route("/list/<int:page>", methods=["GET", "POST"])
def view_lotto_list(page=1):
  model = LottoApiListModel()
  model.setPageInfo(
    page=page,
    # rows_per_page=3,
    # count_per_page=10
  )
  datas = model.getDatas(
    filters={
      "DRWT_NO__OT": 1
    },
    sortings=[
      "DRWT_NO__DESC"
    ]
  )

  return render_template(
    "/views/lotto/list.jinja",
    datas=datas,
    pageInfo=model.Meta.page_info,
    colnames=model.getAlias()
  )

@bp.route("/write", methods=["GET","POST","PUT","DELETE"])
def view_lotto_write():
  method = request.method

  jobListModel = LottoJobListModel()

  if method == "GET":
    crawler_options = jobListModel.getDatas()

    return render_template(
      "/views/"+request.path+".jinja",
      crawler_options=crawler_options
    )

  elif method == "POST": # CREATE
    data = dict(request.form)
    
    return jsonify({
      "success": True,
      "data": data
    })
    
  elif method == "PUT": # UPDATE
    pass

  elif method == "DELETE": # DELETE
    pass

  return render_template("/views/lotto/list.jinja")