from flask import (
    current_app as app,
    render_template
)

@app.route("/", methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def indexMain():
  return render_template("index.html")