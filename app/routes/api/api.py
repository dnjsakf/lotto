from flask import (
    current_app as app,
    render_template,
    jsonify,
    g
)

@app.route("/api/lotto/list", methods=["GET"])
def getApiLottoList():
  datas = g.db.getAllLotto()
  return jsonify({
    "datas": datas
  })

@app.route("/api/lotto/list/<int:page>", methods=["GET"])
def getApiLottoListForPage(page=1):
  datas = g.db.getPageLotto(page)
  total = g.db.getTotalLotto()
  hasNextPage = bool(g.db.getNextPage(page))
  hasPrevPage = bool(g.db.getPrevPage(page))

  return jsonify({
    "datas": datas,
    "size": len(datas),
    "pagination": {
      "page": page,
      "total": total,
      "hasNextPage": hasNextPage,
      "hasPrevPage": hasPrevPage
    }
  })
