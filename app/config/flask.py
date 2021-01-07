from .database import (
  SQLiteConfig,
  OracleConfig
)

class BaseConfig(object):
  TESTING = False
  JSONIFY_PRETTYPRINT_REGULAR = True

class ProductionConfig(BaseConfig):
  SQLITE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(BaseConfig):
  DEV_SERVER_HOST = "localhost"
  DEV_SERVER_PORT = 3000
  DEV_SERVER_THREADED = True
  
  SQLITE_URI = 'sqlite://../app/database/example.db' # 'sqlite:///:memory:'

  ORACLE_DB = "CAMPDB"
  ORACLE_USERNAME = "SYSTEM"
  ORACLE_PASSWORD = "campmaxquad12"
  ORACLE_URL = "localhost"
  ORACLE_PORT = 1521

  SCHEDULER_BACKGROUND = True

class TestingConfig(BaseConfig):
  TESTING = True
