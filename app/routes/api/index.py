from flask import Blueprint, request, jsonify

bp = Blueprint('api', __name__, url_prefix="/api")

@bp.route("", methods=["GET"])
def get_api():
  return jsonify({
    "endpoint": request.endpoint
  })
