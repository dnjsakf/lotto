import traceback

from functools import wraps

class SQLiteDecorator(object):
  def with_cursor(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      _self = args[0]

      conn = _self.getConnection()
      cursor = None
      res = None

      try:
        cursor = conn.cursor()
        res = f(_self, cursor, *args[1:], **kwargs)
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