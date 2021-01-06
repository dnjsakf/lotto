import traceback

from typing import Optional, Union, Iterable, Tuple, Any
from app.utils.fields.Fields import BaseField, ListField, DatetimeField

class BaseModel(object):
  '''
    Options
      - required: 필수값
      - alias
        @ load: alias로 데이터를 탐색하여 저장.
        @ dump: alias로 dictionary 객체 생성.
  '''
  def __init__(self, datas:Optional[Iterable]=None, **kwargs):
    self.__seek = 0
    self.__start = 0
    self.__end = 0
    self.__datas = None

    if datas is not None:
      self.loads(datas)
    else:
      self.load(dict(kwargs))

  def loads(self, datas:list):
    setattr(self, "__seek", 0)
    setattr(self, "__start", 0)
    setattr(self, "__end", len(datas)-1)
    setattr(self, "__datas", datas)

    return self

  def load(self, data:dict):
    '''
      Mapping dictionary to attribute.
    '''
    load_data = dict()
    
    for attrName in dir(self):
      attr = getattr(self, attrName)
      if attrName.startswith("_") or callable(attr):
        continue
      
      if isinstance(attr, BaseField):
        dataKey = attr.getOption("alias", attrName)

        # Default Value
        default_value = None
        call_default_value = attr.getOption("default_value", None)
        
        if isinstance(call_default_value, str) and hasattr(self, call_default_value):
          call_default_value = getattr(self, call_default_value)

        if callable(call_default_value):
          default_value = call_default_value(dataKey, attr)

        # Set Value
        if isinstance(attr, ListField):
          '''
            ListField는 'get_변수명'의 함수를 호출하여 데이터를 생성
          '''
          if hasattr(self, "get_"+attrName):
            call_get_event = getattr(self, "get_"+attrName)
            if callable(call_get_event):
              ModelClass = attr.getOption("model", None)
              model = ModelClass()
              retval = call_get_event(model, attr)
              if isinstance(retval, Iterable):
                attrValue = retval

        else:
          attrValue = data.get(dataKey, data.get(attrName, default_value))

        # Store value on field.
        attr.setValue(attrValue)

      else:
        '''
          BaseField가 아닌 경우, Attribute에 값을 직접 대입
        '''
        dataKey = attrName
        attrValue = data.get(dataKey, None)
        setattr(self, attrName, attrValue)

    # print( load_data )
          
    return self

  def dump(self, data=None):
    '''
      Mapping attribute to dictionary.
    '''
    dump_data = dict()

    for attrName in dir(self):
      attr = getattr(self, attrName)
      if attrName.startswith("_") or callable(attr):
        continue

      if isinstance(attr, BaseField):
        dataKey = attr.getOption("alias", attrName)
                
        if data is not None:
          dataVal = data.get(dataKey if dataKey in data else attrName)
        else:
          dataVal = attr.getValue()

        if dataVal is not None:
          if isinstance(attr, DatetimeField):
            dataVal = attr.strftime(dataVal)

      else:
        dataKey = attrName
        dataVal = attr
        
      dump_data[dataKey] = dataVal

    return dump_data

  def dumps(self):
    if hasattr(self, "__datas"):
      return [ self.dump(data) for data in getattr(self, "__datas") ]
    return None

  def getAttrs(self):
    attrs = list()
    for attrName in dir(self):
      attr = getattr(self, attrName)
      if not callable(attr) and not attrName.startswith("_"):
        attrValue = attr.getValue() if isinstance(attr, BaseField) else attr
        attrs.append((
          attrName,       # Attribute Name
          attrValue,      # Attribute Value
          type(attrValue) # Attribute Type
        ))
    return attrs

  def __iter__(self):
    return self

  def __next__(self):
    seek = getattr(self, "__seek")
    start = getattr(self, "__start")
    end = getattr(self, "__end")
    datas = getattr(self, "__datas")

    if seek <= end:
      data = datas[seek]
      setattr(self, "__seek", seek+1)
      return data
    else:
      raise StopIteration

  def __str__(self):
    return str(self.getAttrs())


class DatabaseModel(BaseModel):
  '''
    기본 컬럼명이나 Methods 외에는 Meta Class에 작성하여 사용
  '''
  class Meta:
    db = None
    schema:Optional[str]
    table:str
    init:Iterable
    symbol:Optional[str]

  def __init__(self, *args, **kwargs):
    # Called parent init method.
    super(DatabaseModel, self).__init__(*args, **kwargs)

    # Meta 기본값 설정
    if not hasattr(self.Meta, "symbol"):
      setattr(self.Meta, "symbol", "?")
    if not hasattr(self.Meta, "init"):
      setattr(self.Meta, "init", [])
    if not hasattr(self.Meta, "limit"):
      setattr(self.Meta, "limit", 10)
    if not hasattr(self.Meta, "offset"):
      setattr(self.Meta, "offset", 0)

    # init에 등록된 함수들을 실행
    if hasattr(self.Meta, "init") and isinstance(self.Meta.init, list):
      for call_name in self.Meta.init:
        call_init = getattr(self, call_name)
        if callable(call_init):
          init_res = call_init()
          if init_res is None:
            continue
          if isinstance(init_res, list):
            self.loads( init_res )
          else:
            self.load( init_res )


  def getPstmt(self, **kwargs):
    attrs = self.getAttrs()
    
    colNames = list()
    symbols = list()
    values = list()
    PKs = list()

    for name, value, _type in attrs:
      if name.startswith("_"):
        continue

      attr = getattr(self, name)

      if isinstance(attr, BaseField):
        ignore = bool(attr.getOption("ignore"))
        if "fillter__ignore" in kwargs and kwargs.get("fillter__ignore", False) != ignore:
          continue

        PK = bool(attr.getOption("PK"))
        if "fillter__PK" in kwargs and kwargs.get("fillter__PK", False) != PK:
          continue
        PKs.append(PK)

      colNames.append(name)
      values.append(value)

      if self.Meta.symbol == ":":
        symbols.append(self.Meta.symbol+name)
      else:
        symbols.append(self.Meta.symbol)

    return ( colNames, symbols, values, PKs )

  def getTableName(self):
    # Set TableName
    schema = None
    table = self.Meta.table
    if hasattr(self.Meta, "schema"):
      schema = getattr(self.Meta, "schema", None)
      if schema is not None:
        table = schema+"."+table

    return table

  def insert(self):
    '''
      DML
        - 데이터 입력
    '''
    colNames, symbols, values, PKs = self.getPstmt(fillter__ignore=False)

    # Set SQL
    SQL = "INSERT INTO "+self.getTableName()+" ("
    SQL += ", ".join(colNames)
    SQL += ") VALUES ("
    SQL += ", ".join(symbols)
    SQL += ")"

    # Execute DML
    return self.executeUpdate(SQL, values)


  def delete(self):
    '''
      DML
        - 데이터 삭제
    '''
    colNames, symbols, values, PKs = self.getPstmt(fillter__PK=True)

    # Set SQL
    SQL = "DELETE FROM "+self.getTableName()
    for idx, ( colName, symbol ) in enumerate(zip(colNames, symbols)):
      SQL += ( " WHERE " if idx == 0 else " AND "  ) + colName + " = " + symbol

    # Execute DML
    return self.executeUpdate(SQL, values)


  def update(self):
    '''
      DML
        - 데이터 수정
    '''
    colNames, symbols, values, PKs = self.getPstmt(fillter__ignore=False)

    setters = list()
    conds = list()
    upd_values = list()

    # Separator Setters / Condtitions
    for colName, symbol, value, PK in zip(colNames, symbols, values, PKs):
      if not PK:
        setters.append(( colName, symbol, value ))
      else:
        conds.append(( colName, symbol, value ))

    # Set SQL
    SQL = "UPDATE " + self.getTableName()

    # Set Setters
    for idx, ( colName, symbol, value ) in enumerate(setters):
      SQL += ( " SET " if idx == 0 else " , "  ) + colName + " = " + symbol
      upd_values.append( value )

    # Set Conditions
    for idx, ( colName, symbol, value ) in enumerate(conds):
      SQL += ( " WHERE " if idx == 0 else " AND "  ) + colName + " = " + symbol
      upd_values.append( value )

    # Execute DML
    return self.executeUpdate(SQL, upd_values)

  
  def merge(self):
    print("[merge] start")
    updatecount = 0

    print("[select] start")
    selected = self.getData()
    print("[select] finish")

    if selected is None:
      print("[insert] start")
      updatecount = self.insert()
      print("[insert] finish")
    else:
      print("[update] start")
      updatecount = self.update()
      print("[update] finish")

    print("[merge] finish")

    return updatecount


  def executeQuery(self, SQL, values=list(), fetchone:Optional[bool]=False, record_to_dict:Optional[bool]=True):
    '''
      DQL(Data Query Language)
        - select
    '''
    selected = None

    print( SQL )

    try:
      conn = self.Meta.db.ensure(record_to_dict=record_to_dict)
      cursor = conn.cursor()
      cursor.execute(SQL, values)

      if fetchone:
        selected = cursor.fetchone()
      else:
        selected = cursor.fetchall()

      cursor.close()

    except Exception as e:
      traceback.print_exc()

    finally:
      self.Meta.db.close()

    return selected


  def executeUpdate(self, SQL, values=None):
    '''
      DML(Data Manipulation Language)
        - insert, delete, update
    '''
    updatecount = 0

    conn = None
    try:
      conn = self.Meta.db.getConnection()
      cursor = conn.cursor()
      cursor.execute(SQL, values)
      cursor.close()

      updatecount = cursor.rowcount

      conn.commit()

    except Exception as e:
      traceback.print_exc()
      conn.rollback()

    finally:
      self.Meta.db.close()
      
    return updatecount

  
  def getData(self):
    '''
      DQL
        - 데이터 조회
    '''
    colNames, symbols, values, PKs = self.getPstmt(fillter__ignore=False)

    # Set SQL
    SQL = "SELECT "+ ",".join(colNames)+" FROM "+self.getTableName()
    sel_values = list()

    # Set Conditions
    SQL += " WHERE 1=1"
    for idx, ( colName, symbol, value, PK ) in enumerate(zip(colNames, symbols, values, PKs)):
      if PK:
        SQL += ( " AND " + colName + " = " + symbol )
        sel_values.append( value )

    # Execute DML
    res = self.executeQuery(SQL, sel_values)
    if res is not None and len(res) > 0:
      return res.pop()

    return None


  def getDatas(self, conditions:Tuple[str, Any]=tuple()):
    '''
      DQL
        - 데이터 목록 조회
    '''
    colNames, symbols, values, PKs = self.getPstmt(fillter__ignore=False)

    # Set SQL
    SQL = "SELECT "+ ",".join(colNames)+" FROM "+self.getTableName()
    sel_values = list()

    # Set Conditions
    SQL += " WHERE 1=1"
    for idx, ( colName, symbol, value, PK ) in enumerate(zip(colNames, symbols, values, PKs)):
      if colName in conditions:
        SQL += ( " AND " + colName + " = " + symbol )
        sel_values.append( value )

    # Execute DML
    res = self.executeQuery(SQL, sel_values)

    return res
    