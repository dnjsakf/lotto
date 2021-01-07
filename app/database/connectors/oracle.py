import logging
import traceback
import cx_Oracle

from typing import Optional, Union, Callable

logging.basicConfig()
logger = logging.getLogger("connector")
logger.setLevel(logging.DEBUG)

class OracleConnection(cx_Oracle.Connection):
  def cursor(self):

    record_to_dict = None
    if hasattr(self, "record_to_dict"):
      record_to_dict = getattr(self, "record_to_dict")

    return OracleCursor(conn=self, record_to_dict=record_to_dict)

class OracleCursor(cx_Oracle.Cursor):
  def __init__(self, conn:OracleConnection, record_to_dict:Callable=None):
    self.record_to_dict = record_to_dict

    super(OracleCursor, self).__init__(conn)

  def fetchone(self):
      return super(OracleCursor, self).fetchone()
      
  def fetchall(self):
      return super(OracleCursor, self).fetchall()

  def execute(self, *args, **kwargs):
    cursor = super(OracleCursor, self).execute(*args, **kwargs)

    if cursor is not None and hasattr(self, 'record_to_dict') and callable(self.record_to_dict):
      cursor.rowfactory = self.record_to_dict(cursor)

    return cursor


class OracleConnector(object):

  conn:OracleConnection = None

  @classmethod
  def init(
      cls,
      host:Optional[str]="localhost",
      port:Union[(str,int)]=1521,
      db:str=None,
      username:Optional[str]=None,
      password:Optional[str]=None,
      **options
    ):
    
    cls.host = host
    cls.port = str(port)
    cls.db = db
    cls.username = username
    cls.password = password
    cls.encoding = options.get("encoding", "UTF-8")
    cls.options = options

  def __init__(self, db=None, *args, **kwargs):
    # if db is not None:
    #   self.db = db
    # self.conn = self.getConnection()
    pass

  def getConnection(self, record_to_dict=True) -> OracleConnection:
    logger.info("[getConnection] start")
    if self.conn is None:
      try:
        self.conn = OracleConnection(
          self.username,
          self.password,
          self.host+":"+self.port+"/"+self.db,
          encoding=self.encoding
        )

        if record_to_dict:
          self.conn.record_to_dict = self.record_to_dict

      except Exception as e:
        traceback.print_exc()
    logger.info("[getConnection] finish")
    return self.conn

  def ensure(self, *args, **kwargs) -> OracleConnection:
    logger.info("[ensure] start")
    if self.conn is not None:
      self.close()
    logger.info("[ensure] finish")
    return self.getConnection(*args, **kwargs)

  def close(self):
    logger.info("[close] start")
    try:
      if self.conn is not None:
        self.conn.rollback()
        self.conn.close()
    except Exception as e:
      traceback.print_exc()

    finally:
      self.conn = None

    logger.info("[close] finish")

  def record_to_dict(self, cursor) -> Callable:
    column_names = [ col[0] for col in cursor.description ]

    def mapping(*args):
      return dict(zip(column_names, args))

    return mapping