from flask import Flask
from flask_cors import CORS

def create_app(option={}):
  app = Flask( __name__, **option )
  
  with app.app_context():
    # Set CORS
    CORS(app=app, resources={
      r"*": { "origin": "*" }
    })
    
    # Set Routes
    from .routes import routes
  
  return app