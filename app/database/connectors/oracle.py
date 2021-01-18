import logging
import traceback
import cx_Oracle

from typing import (
  Optional, Union, Any, Callable, Iterable, List, Dict, Tuple
)

logging.basicConfig()
logger = logging.getLogger("connector")
logger.setLevel(logging.DEBUG)

# Samples
# https://github.com/oracle/python-cx_Oracle/blob/master/samples/SetupSamples.py

class OracleConnection(cx_Oracle.Connection):
  def cursor(self):

    record_to_dict = None
    if hasattr(self, "record_to_dict"):
      record_to_dict = getattr(self, "record_to_dict")

    return OracleCursor(conn=self, record_to_dict=record_to_dict)

class OracleSessionPool(cx_Oracle.SessionPool):
  def __init__(self, *args, **kwargs):
    super(OracleSessionPool, self).__init__(*args, **kwargs)

  def acquire(self, *args, **kwargs):
    return OracleConnection(pool=self, *args, **kwargs)

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
  pool:OracleSessionPool = None

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

    if cls.pool is not None:
      cls.pool.close()

    cls.pool = OracleSessionPool(
      cls.username,
      cls.password,
      cls.host+":"+cls.port+"/"+cls.db,
      min=2, max=5, increment=1,
      encoding=cls.encoding
    )
  
  def __init__(self, db=None, *args, **kwargs):
    # if db is not None:
    #   self.db = db
    # self.conn = self.getConnection()
    pass
  
  @classmethod
  def getConnection(cls, pool=None, record_to_dict=True) -> OracleConnection:
    logger.info("[getConnection] start %s" % (pool))
    logger.info( cls.conn is None )
    if cls.conn is None:
      try:
        # Using Sigle Connection
        # cls.conn = OracleConnection(
        #   cls.username,
        #   cls.password,
        #   cls.host+":"+cls.port+"/"+cls.db,
        #   encoding=cls.encoding
        # )
        cls.conn = cls.pool.acquire(tag=pool) # Using Session Pool
        cls.conn.autocommit = False
        cls.conn.tag = pool

        if record_to_dict:
          cls.conn.record_to_dict = cls.record_to_dict

      except Exception as e:
        traceback.print_exc()
    logger.info("[getConnection] finish %s " % ( cls.conn.tag ))
    return cls.conn

  @classmethod
  def ensure(cls, *args, **kwargs) -> OracleConnection:
    logger.info("[ensure] start")
    if cls.conn is not None:
      cls.close()
    logger.info("[ensure] finish")
    return cls.getConnection(*args, **kwargs)

  @classmethod
  def close(cls):
    logger.info("[close] start")
    try:
      if cls.conn is not None:
        cls.conn.rollback()
        cls.conn.close()
      # cls.pool.release(cls.conn)
    except Exception as e:
      traceback.print_exc()

    finally:
      cls.conn = None

    logger.info("[close] finish")

  @classmethod
  def record_to_dict(cls, cursor) -> Callable:
    column_names = [ col[0] for col in cursor.description ]

    def mapping(*args):
      return dict(zip(column_names, args))

    return mapping

  @classmethod
  def executeQuery(
    cls,
    SQL:str,
    values:Union[Dict,List,Tuple]=tuple(),
    fetchone:bool=False
    ) -> Iterable:

    logger.info( SQL )

    conn = None
    cursor = None
    records = None

    try:
      conn = cls.getConnection()
      cursor = conn.cursor()
      cursor.execute(SQL, values)

      if fetchone:
        records = cursor.fetchone()
      else:
        records = cursor.fetchall()

      cursor.close()

    except Exception as e:
      traceback.print_exc()
      
    finally:
      cls.close()

    return records

  @classmethod
  def executeUpdate(
      cls,
      SQL:str,
      values:Union[Dict,List,Tuple]=tuple(),
      pool:str=None,
      commit:bool=False
      ) -> int:
    '''
      DML(Data Manipulation Language)
        - insert, delete, update
    '''
    
    conn = None
    cursor = None
    updatecount = 0

    try:
      conn = cls.getConnection(pool=pool)
      cursor = conn.cursor()
      cursor.execute(SQL, values)

      updatecount = cursor.rowcount
      
      cursor.close()
      conn.commit()

      # if pool is not None and commit:
      #   conn.commit()
      # elif pool is None:
      #   conn.commit()

    except Exception as e:
      traceback.print_exc()
      conn.rollback()

    finally:
      cls.close()
      # if pool is not None and commit:
      #   cls.close()
      # elif pool is None:
      #   cls.close()
      
    return updatecount
    
  @classmethod
  def executeMany(
      cls,
      SQL:str,
      values:Union[Dict,List,Tuple]=tuple(),
      pool:str=None,
      commit:bool=False
      ):
    '''
      Bulk DML(Data Manipulation Language)
        - insert, delete, update
    '''
    conn = None
    cursor = None
    updatecount = 0

    try:
      conn = cls.getConnection()
      cursor = conn.cursor()
      cursor.executemany(SQL, values)

      updatecount = cursor.rowcount

      cursor.close()
      conn.commit()

    except Exception as e:
      traceback.print_exc()
      conn.rollback()

    finally:
      cls.close()
      
    return updatecount

  @classmethod
  def executeFunc(
      cls,
      name:str,
      rettype:Any,
      args:List,
      pool:str=None
      ):
    '''
      Call Stored Functions
    '''
    conn = None
    cursor = None
    retval = None

    try:
      conn = cls.getConnection(pool=pool)
      cursor = conn.cursor()
      retval = cursor.callfunc(name, rettype, args)
      cursor.close()
      conn.commit()

    except Exception as e:
      traceback.print_exc()
      conn.rollback()

    finally:
      cls.close()
      
    return retval
