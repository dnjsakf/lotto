from flask import Blueprint, render_template, jsonify
from app.models.oracle import LottoApiListModel

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("/", methods=["GET", "POST"])
def view_index(page=1):
  return render_template("index.html")

@bp.route("/list", methods=["GET", "POST"])
@bp.route("/list<int:page>", methods=["GET", "POST"])
def view_list(page=1):
  model = LottoApiListModel()
  model.setPageInfo(
    page=page,
    rows_per_page=3,
    count_per_page=10
  )

  datas = model.loads(model.getDatas()).dumps()

  return render_template("list.html", datas=datas, pageInfo=model.Meta.page_info)