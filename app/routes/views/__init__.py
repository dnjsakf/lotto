from flask import current_app as app
from .index import bp as view_index
from .lotto import bp as view_lotto
from .sched import bp as view_sched

def register_views():
  app.register_blueprint(view_index, url_prefix="/")
  app.register_blueprint(view_lotto, url_prefix="/lotto")
  app.register_blueprint(view_sched, url_prefix="/sched")