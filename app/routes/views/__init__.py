from flask import current_app as app
from .index import bp as view_index
from .lotto import bp as view_lotto

def register_views():
  app.register_blueprint(view_index, url_prefix="/")
  app.register_blueprint(view_lotto, url_prefix="/lotto")