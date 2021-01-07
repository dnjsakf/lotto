from flask import current_app as app
from .index import bp as view_index

def register_views():
  app.register_blueprint(view_index, url_prefix="/")