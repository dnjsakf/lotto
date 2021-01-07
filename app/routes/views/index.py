from flask import Blueprint, render_template, jsonify
from app.models.oracle import LottoApiListModel

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("/", methods=["GET", "POST"])
@bp.route("/<int:page>", methods=["GET", "POST"])
def view_index(page=1):
  model = LottoApiListModel()
  model.setPageInfo(
    page=page,
    rows_per_page=3,
    count_per_page=10
  )

  datas = model.loads(model.getDatas()).dumps()

  return render_template("list.html", datas=datas, pageInfo=model.Meta.page_info)