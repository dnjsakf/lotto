from flask import (
    current_app as app,
    render_template,
    jsonify,
    g
)

@app.route("/", methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def indexMain(path=None):
  return render_template("index.html")
