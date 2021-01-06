from .database import (
  SQLiteConfig,
  OracleConfig
)

class BaseConfig(object):
  DEBUG = False
  TESTING = False
  DATABASE_URI = 'sqlite://../app/database/example.db' # 'sqlite:///:memory:'

class ProductionConfig(BaseConfig):
  DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(BaseConfig):
  DEBUG = True

class TestingConfig(BaseConfig):
  TESTING = True
