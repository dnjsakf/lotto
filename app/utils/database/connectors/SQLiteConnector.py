import traceback
import sqlite3
import pandas as pd
import numpy as np
import datetime

from functools import wraps

from .connectors import BaseConnector

class LottoDataFormat(object):
  def __init__(self, datas):
    self.index = 0
    self.size = len(datas)
    self.datas = datas

  def __iter__(self):
    self.index = 0
    return self
  
  def __next__(self):
    if self.index >= self.size:
      raise StopIteration

    data = self.datas[self.index]

    if isinstance(data[1], pd._libs.tslibs.timestamps.Timestamp):
      data[1] = data[1].strftime('%Y%m%d%H%M%S')

    self.index += 1

    return data
    

def with_cursor(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    _self = args[0]

    conn = _self.getConnection()
    cursor = None
    res = None

    try:
      cursor = conn.cursor()
      res = f(*args, cursor, **kwargs)
      cursor.close()
      
      conn.commit()
    
    except Exception as e:
      traceback.print_exc()
      if conn is not None:
        conn.rollback()

    finally:
      try:
        if cursor is not None:
          cursor.close()

      except Exception as e:
        traceback.print_exc()
      
      finally:
        cursor = None

    return res
  return wrapper


class SQLiteConnector(BaseConnector):

  conn = None
  db = None
  
  def __init__(self, db="example.db", **args):
    try:
      self.db = db
      self.initDropTable()
      self.initCreateTable()
    
    except Exception as e:
      traceback.print_exc()

  def getConnection(self):
    if self.conn is None:
      return sqlite3.connect(self.db)
    return self.conn
    
  @with_cursor
  def initDropTable(self, cursor: sqlite3.Cursor ):
    cursor.execute('DROP TABLE LOTTO_RSLT')
  
  @with_cursor
  def initCreateTable(self, cursor: sqlite3.Cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS LOTTO_RSLT (
      NO              INTEGER
      , WIN_DATE      TEXT
      , WIN_CNT_1ST   INTEGER
      , WIN_AMT_1ST   INTEGER
      , WIN_CNT_2ND   INTEGER
      , WIN_AMT_2ND   INTEGER
      , WIN_CNT_3RD   INTEGER
      , WIN_AMT_3RD   INTEGER
      , WIN_CNT_4TH   INTEGER
      , WIN_AMT_4TH   INTEGER
      , WIN_CNT_5TH   INTEGER
      , WIN_AMT_5TH   INTEGER
      , NUM1          INTEGER
      , NUM2          INTEGER
      , NUM3          INTEGER
      , NUM4          INTEGER
      , NUM5          INTEGER
      , NUM6          INTEGER
      , BONUS         INTEGER
      , LOAD_DTTM     TEXT
    )
    ''')

  @with_cursor
  def initLoadData(self, cursor: sqlite3.Cursor, filename="lotto_1-940.xlsx"):
    xslx = pd.read_excel(filename)
    datas = np.array(xslx)

    iters = LottoDataFormat(datas)

    print( iters.size )

    cursor.executemany('''
      INSERT INTO LOTTO_RSLT (
        NO
        , WIN_DATE
        , WIN_CNT_1ST
        , WIN_AMT_1ST
        , WIN_CNT_2ND
        , WIN_AMT_2ND
        , WIN_CNT_3RD
        , WIN_AMT_3RD
        , WIN_CNT_4TH
        , WIN_AMT_4TH
        , WIN_CNT_5TH
        , WIN_AMT_5TH
        , NUM1
        , NUM2
        , NUM3
        , NUM4
        , NUM5
        , NUM6
        , BONUS
        , LOAD_DTTM
      ) VALUES (
        ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , ?
        , strftime('%Y%m%d%H%M%S','now')
      )
    ''', iters)

    print("Inserted: %d" % cursor.rowcount )

  @with_cursor
  def getLast(self, cursor):
      cursor.execute("SELECT * FROM LOTTO_RSLT")
      print( cursor.fetchone() )


