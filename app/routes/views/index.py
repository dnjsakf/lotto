from flask import Blueprint, render_template

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("/", methods=["GET", "POST"])
def view_index(page=1):
  return render_template("index.html")
