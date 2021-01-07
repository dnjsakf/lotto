from flask import Blueprint, jsonify
from app.models.oracle import LottoApiModel

bp = Blueprint('api_lotto', __name__, url_prefix="/api/lotto")

@bp.route("/list", methods=["GET"])
def get_lotto_api_list():
  model = LottoApiModel()
  datas = model.loads(model.getDatas()).dumps()

  return jsonify({
    "datas": datas
  })

# @bp.route("/list/<int:page>", methods=["GET"])
# def getApiLottoListForPage(page=1):
#   countForPage = 10
  
#   db = LottoService()

#   datas = db.getPageLotto(page, countForPage)
#   total = db.getTotalLotto()
#   hasNextPage = bool(db.getNextPage(page, countForPage))
#   hasPrevPage = bool(db.getPrevPage(page, countForPage))

#   return jsonify({
#     "datas": datas,
#     "size": len(datas),
#     "pagination": {
#       "countForPage": countForPage,
#       "page": page,
#       "total": total,
#       "hasNextPage": hasNextPage,
#       "hasPrevPage": hasPrevPage
#     }
#   })
