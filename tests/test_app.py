import pytest

from app.database.connectors import SQLiteConnector
from app.scheduler.launchers import JobLauncher

from flask import Flask
from app.routes.api.sched import bp

@pytest.fixture(scope='module') # Multiple Used
def client():
  SQLiteConnector.init(db="./app/database/example.db")

  app = Flask(__name__)
  app.register_blueprint(bp)
  app.config["launcher"] = JobLauncher(background=True)
  app.config["launcher"].start()

  with app.test_client() as client:
    yield client
    
  print("close app")

# @pytest.mark.skip
# def create_app(self, client):
#   print( client )
