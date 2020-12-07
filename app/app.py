from flask import Flask
from flask_cors import CORS
from app.utils.database.connectors import SQLiteConnector

def create_app(option={}):
  app = Flask( __name__, **option )
  
  with app.app_context():
    # Set Routes
    from .routes import routes

    # Set CORS
    CORS(app=app, resources={
      r"*": { "origin": "*" }
    })

    handle_request()
  
  return app

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
        g.db = SQLiteConnector("./app/database/example.db")
  
  @app.teardown_appcontext
  def close_db(error=None, *args, **kwargs):
    app.logger.info("teardown_appcontext")
    db = g.pop('db', None)
    if db is not None:
      db.close()