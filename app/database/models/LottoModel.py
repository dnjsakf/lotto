import sqlite3

from app.database.connectors import SQLiteConnector
from app.database.decorators import SQLiteDecorator as conn

class LottoModel(SQLiteConnector):
  @conn.with_cursor
  def getLastLotto(self, cursor: sqlite3.Cursor):
    cursor.execute('''
    SELECT *
      FROM LOTTO_RSLT
     WHERE 1=1
     ORDER BY NO DESC
     LIMIT 1
    ''')
    return cursor.fetchone()

  @conn.with_cursor
  def getAllLotto(self, cursor: sqlite3.Cursor):
    cursor.execute('''
    SELECT * 
      FROM LOTTO_RSLT
     WHERE 1=1
     ORDER BY NO DESC
    ''')
    return cursor.fetchall()

  @conn.with_cursor
  def getPageLotto(self, cursor: sqlite3.Cursor, page=1, countForPage=10):
    offset = ((page - 1) * countForPage)
    if offset < 0:
      return []

    cursor.execute('''
    SELECT * 
      FROM LOTTO_RSLT 
     WHERE 1=1
     ORDER BY NO DESC 
     LIMIT %d
     OFFSET %d
    ''' % ( countForPage, offset ))
    return cursor.fetchall()

  @conn.with_cursor
  def getTotalLotto(self, cursor: sqlite3.Cursor):
    cursor.execute('''
    SELECT COUNT(1) AS TOTAL_COUNT
     FROM LOTTO_RSLT
    ''')
    return cursor.fetchone().get("TOTAL_COUNT")
    