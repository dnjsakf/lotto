from flask import Blueprint, render_template

bp = Blueprint("main", __name__, url_prefix="/")

@bp.route("/", methods=["GET", "POST"])
@bp.route("/<path:path>", methods=["GET", "POST"])
def indexMain(path=None):
  return render_template("index.html")

