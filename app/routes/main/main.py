from flask import (
    current_app as app,
    render_template,
    jsonify,
    g
)

from app.utils.database.connectors import SQLiteConnector

@app.route("/", methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
def indexMain(path=None):
  return render_template("index.html")

@app.route("/data", methods=["GET"])
def getData():
  return jsonify({
    "datas": g.db.getAll()
  })

@app.route("/data/<int:page>", methods=["GET"])
def getDataForPage(page=1):
  return jsonify({
    "datas": g.db.getPage(page)
  })
