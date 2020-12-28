import os
ROOT_PATH = 

class Config(object):
  DEBUG = False
  TESTING = False
  DATABASE_URI = 'sqlite://../app/database/example.db' # 'sqlite:///:memory:'

class ProductionConfig(Config):
  DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
  DEBUG = True

class TestingConfig(Config):
  TESTING = True