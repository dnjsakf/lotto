import logging
import traceback
import sqlite3

class SQLiteConnection(sqlite3.Connection):
  def cursor(self):
    return SQLiteCursor(self)

class SQLiteCursor(sqlite3.Cursor):
  pass

class SQLiteConnector(object):

  conn:SQLiteConnection = None
  db = "example.db"

  @classmethod
  def init(cls, db=None, *args, **kwargs):
    if db is not None:
      cls.db = db

  def __init__(self, db=None, *args, **kwargs):
    if db is not None:
      self.db = db
    self.conn = self.getConnection()

  def getConnection(self) -> sqlite3.Connection:
    if self.conn is None:
      try:
        self.conn = sqlite3.connect(self.db)
        self.conn.row_factory = self.make_dicts
      except Exception as e:
        traceback.print_exc()

    return self.conn

  def ensure(self):
    if self.conn is not None:
      self.close()
    return self.getConnection()

  def close(self):
    try:
      if self.conn is not None:
        self.conn.close()
    except Exception as e:
      traceback.print_exc()
    finally:
      self.conn = None
    
  @staticmethod
  def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))
