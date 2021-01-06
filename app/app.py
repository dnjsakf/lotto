import os

from flask import Flask
from flask_cors import CORS

from app.database.connectors import SQLiteConnector, OracleConnector
from app.scheduler.launchers import JobLauncher

def create_app(ROOT_PATH="./"):

  # Create Flask APP
  app = Flask(__name__, **{
    "static_url_path": "/static/",
    "static_folder": os.path.join(ROOT_PATH, "src/dist"),
    "template_folder": os.path.join(ROOT_PATH, "src/dist"),
  })
  
  # Set Configuration
  FLASK_ENV = os.environ.get("FLASK_ENV", "PRODUCTION").upper()
  if FLASK_ENV == "DEVELOPMENT":
    app.config.from_object("app.config.flask.DevelopmentConfig")
  else:
    app.config.from_object("app.config.flask.ProductionConfig")

  # Set Configguration for Launcher
  app.config["launcher"] = JobLauncher(background=True)

  # Set Initialize for Database
  SQLiteConnector.init(db=app.config.get("DATABASE_URI"))
  OracleConnector.init(db="CAMPDB", username="SYSTEM", password="campmaxquad12")
  
  with app.app_context():
    # Set Routes
    register_blueprint(app)

    # Set CORS
    CORS(app=app, resources={
      r"*": { "origin": "*" }
    })

    # Set Request Handlers
    # handle_request()
  
  return app


def register_blueprint(app):
  from .routes import bp as bp_main
  from .routes.api import bp as bp_api
  from .routes.api.lotto import bp as bp_api_lotto
  from .routes.api.sched import bp as bp_api_sched

  # Set /
  app.register_blueprint(bp_main, url_prefix="/")

  # Set /api
  app.register_blueprint(bp_api, url_prefix="/api")
  app.register_blueprint(bp_api_lotto, url_prefix="/api/lotto")
  app.register_blueprint(bp_api_sched, url_prefix="/api/sched")


def handle_request():
  from flask import (
    g,
    url_for, 
    request,
    current_app as app
  )

  @app.before_request
  def get_db(error=None):
    app.logger.info("before_request")
    if request.endpoint != "static":
      if "db" not in g:
        g.db = SQLiteConnector(app.config.get("DATABASE_URI"))
  
  @app.teardown_appcontext
  def close_db(error=None, *args, **kwargs):
    app.logger.info("teardown_appcontext")
    db = g.pop('db', None)
    if db is not None:
      db.close()