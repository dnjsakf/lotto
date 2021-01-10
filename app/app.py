import os
import dotenv

from flask import Flask
from flask_cors import CORS

from app.database.connectors import SQLiteConnector, OracleConnector
from app.scheduler.launchers import JobLauncher

# Set Constraints
APP_PATH = os.path.abspath(os.path.dirname(__file__))

def create_app():
  # Create Flask APP
  app = Flask(__name__)
  app.static_url_path = "/static/"
  app.static_folder = os.path.join(APP_PATH, "static")
  app.template_folder = os.path.join(APP_PATH, "templates")
  app.url_map.strict_slashes = False

  # Set Environment Variables
  dotenv.load_dotenv(dotenv_path=".env")
  
  # Set Configuration Default
  FLASK_ENV = os.environ.get("FLASK_ENV", "production").lower()
  if FLASK_ENV == "development":
    app.config.from_object("app.config.flask.DevelopmentConfig")
  else:
    app.config.from_object("app.config.flask.ProductionConfig")

  # Get Configuration Namespace
  SCHEDULER_CONFIG = app.config.get_namespace("SCHEDULER_")
  SQLITE_DATABASE_CONFIG = app.config.get_namespace("SQLITE_")
  ORACLE_DATABASE_CONFIG = app.config.get_namespace("ORACLE_")

  # Set Configuration for SECRET_KEY
  SECRET_KEY = app.config.get("SECRET_KEY") or os.environ.get("SECRET_KEY", None)
  if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Flask application")
  app.config["SECRET_KEY"] = SECRET_KEY

  # Set Configuration for Scheduler
  app.config["launcher"] = JobLauncher(**SCHEDULER_CONFIG)

  # Set Initialize for Database
  SQLiteConnector.init(**SQLITE_DATABASE_CONFIG)
  OracleConnector.init(**ORACLE_DATABASE_CONFIG)
  
  with app.app_context():
    # Set Middlewares
    handle_middleware()

    # Set Request Handlers
    handle_request()
    
    # Set Templates
    handle_templates()

    # Set Routes
    register_routes()
  
  return app


def handle_middleware():
  from flask import current_app as app

  # Set CORS
  CORS(app=app, resources={
    r"*": { "origin": "*" }
  })


def handle_request():
  from flask import (
    current_app as app,
    redirect,
    request,
    url_for
  )

  @app.before_request
  def clear_trailing():
    path = request.path 
    if path != '/' and path.endswith('/'):
      return redirect(path[:-1])

  def dated_url_for(endpoint, **values):
    if endpoint == "static":
      filename = values.get('filename', None)
      if filename:
        file_path = os.path.join(app.static_folder, filename)
        values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

  @app.context_processor
  def override_url_for():
    return dict(url_for=dated_url_for)

def handle_templates():
  from flask import current_app as app

  @app.template_filter("formatdatetime")
  def format_datetime(value):
    print( value )
    if value is None:
      return ""

    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    value = datetime.fromtimestamp(int(value / 1000)) + offset

    return value.strftime('%Y-%m-%d %H:%M:%S')

def register_routes():
  from .routes.views import register_views
  from .routes.api import register_api

  register_views()
  register_api()
