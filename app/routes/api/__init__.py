
from flask import current_app as app

from .index import bp as api_index
from .lotto import bp as api_lotto
from .sched import bp as api_sched

def register_api():
  app.register_blueprint(api_index, url_prefix="/api")
  app.register_blueprint(api_lotto, url_prefix="/api/lotto")
  app.register_blueprint(api_sched, url_prefix="/api/sched")