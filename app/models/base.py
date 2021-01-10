import traceback

from typing import Optional, Union, Iterable, Tuple, List, Any
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

  def getAttrs(self):
    attrs = list()
    for attrName in dir(self):
      attr = getattr(self, attrName)
      if not callable(attr) and not attrName.startswith("_"):
        if isinstance(attr, BaseField):
          attrs.append((attrName, attr.getOption("alias", None)))
        else:
          attrs.append((attrName, None))
    return attrs

  def getAlias(self):
    return [ alias or attr for attr, alias in self.getAttrs() ]

  def loads(self, datas:list):
    attrNames = self.getAttrs()

    temp = list()
    for data in datas:
      temp_dict = dict()
      for attrName, alias in attrNames:
        temp_dict[attrName] = data.get(alias) or data.get(attrName)
      temp.append(temp_dict)

    setattr(self, "__seek", 0)
    setattr(self, "__start", 0)
    setattr(self, "__end", len(temp)-1)
    setattr(self, "__datas", temp)

    return self

  def load(self, data:dict):
    '''
      Mapping dictionary to attribute.
    '''
    load_data = dict()
    
    for attrName, alias in self.getAttrs():
      
      attr = getattr(self, attrName)

      if isinstance(attr, BaseField):
        dataKey = alias or attrName

        # Default Value
        default_value = None
        call_default_value = attr.getOption("default_value", None)
        
        if isinstance(call_default_value, str) and hasattr(self, call_default_value):
          call_default_value = getattr(self, call_default_value)

        if callable(call_default_value):
          default_value = call_default_value(attrName, attr)

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
          attrValue = data.get(alias) or data.get(attrName)

        # Store value on field.
        attr.setValue(attrValue or default_value)

      else:
        '''
          BaseField가 아닌 경우, Attribute에 값을 직접 대입
        '''
        dataKey = attrName
        default_value = None
        attrValue = data.get(dataKey, default_value)
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

  def dumps(self, datas=None):
    if hasattr(self, "__datas"):
      return [ self.dump(data) for data in getattr(self, "__datas") ]
    return None

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

    for attrName, alias in attrs:
      if attrName.startswith("_"):
        continue

      attr = getattr(self, attrName)
      value = None

      if isinstance(attr, BaseField):
        value = attr.getValue()

        ignore = bool(attr.getOption("ignore"))
        if "fillter__ignore" in kwargs and kwargs.get("fillter__ignore", False) != ignore:
          continue

        PK = bool(attr.getOption("PK"))
        if "fillter__PK" in kwargs and kwargs.get("fillter__PK", False) != PK:
          continue
        PKs.append(PK)

      else:
        value = attr

      colNames.append(attrName)
      values.append(value)

      if self.Meta.symbol == ":":
        symbols.append(self.Meta.symbol+attrName)
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

      if hasattr(self.Meta, "description"):
        setattr(self.Meta, "description", cursor.description)

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
    
  def executeMany(self, SQL, values=None):
    '''
      DML(Data Manipulation Language) Bulk
        - insert, delete, update
    '''
    updatecount = 0

    conn = None
    try:
      conn = self.Meta.db.getConnection()
      cursor = conn.cursor()
      cursor.executemany(SQL, values)
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


  def insertMany(self):
    '''
      DML
        - 데이터 입력
    '''
    colNames, symbols, values, PKs = self.getPstmt(fillter__ignore=False)

    # values = list()
    # symbols = [ ":"+str(idx) for idx in range(1, len(colNames)+1) ]

    if hasattr(self, "__datas"):
      values = getattr(self, "__datas")

    # Set SQL
    SQL = "INSERT INTO "+self.getTableName()+" ("
    SQL += ", ".join(colNames)
    SQL += ") VALUES ("
    SQL += ", ".join(symbols)
    SQL += ")"

    print( SQL )
    print( symbols )
    print( values )

    # Execute DML
    return self.executeMany(SQL, values)


  # For list model
  def getDatas(self,
    filters:Tuple[dict]=dict(), # <COLUMN NAME>__<OPERATION> = VALUE
    sortings:Iterable[str]=list(), # # <COLUMN NAME>__<ORDER TYPE>
    dump=True
    ):
    '''
      DQL
        - 데이터 목록 조회
    '''
    column_names, symbols, values, PKs = self.getPstmt(fillter__ignore=False)

    conditions:List(str) = list()
    sorting:List(Tuple(str, str)) = list()
    sel_values = list()

    from_num = (self.Meta.page_info.get("rows_per_page") * ( self.Meta.page_info.get("page") - 1 )) + 1
    to_num = self.Meta.page_info.get("rows_per_page") * self.Meta.page_info.get("page")

    # Set Conditions
    if filters is not None:
      for filter_name, filter_value in filters.items():
        colname = filter_name.split("__")[0]
        operator = " = "

        if filter_name.endswith("__EQ"):
          operator = " = "
        elif filter_name.endswith("__LT"):
          operator = " < "
        elif filter_name.endswith("__OT"):
          operator = " > "

        conditions.append("AND " + colname + operator + self.Meta.symbol+colname)
        sel_values.append(filter_value)

    # Set Sorting
    if sortings is not None:
      for sorting_name in sortings:
        colname = sorting_name.split("__")[0]
        operator = " ASC "

        if sorting_name.endswith("__DESC"):
          operator = "DESC"
        
        sorting.append(colname+" "+operator)

    # Main SQL
    SOURCE_SQL = '''
        SELECT {columns}
          FROM {table}
         WHERE 1=1
           {conditions}
    '''.format(
      columns=",".join(column_names),
      table=self.getTableName(),
      conditions=" ".join(conditions)
    )
    if len(sorting) > 0:
      SOURCE_SQL += '''
         ORDER BY {sorting}
      '''.format(sorting=",".join( sort for sort in sorting ))

    # Page Info SQL
    if hasattr(self.Meta, "page_info"):
      TOTAL_SQL = '''
      WITH TOTAL_OBJ AS (
        {source}
      )
      SELECT COUNT(1) AS TOTAL_COUNT
        FROM TOTAL_OBJ
      '''.format(
        source=SOURCE_SQL
      )
      res = self.executeQuery(TOTAL_SQL, sel_values, fetchone=True)

      self.setPageInfo(
        total_count=res.get("TOTAL_COUNT")
      )

    if len(sorting) == 0:
      sorting.append(column_names[0]+" ASC")

    # Page Data SQL
    PAING_SQL = '''
      WITH SOURCE_OBJ AS (
        {source}
      ), SORT_OBJ AS (
        SELECT T1.*
             , ROW_NUMBER() OVER( ORDER BY {sorting} ) AS RN
          FROM SOURCE_OBJ T1
         WHERE 1=1
      )
      SELECT {columns}
        FROM SORT_OBJ
       WHERE 1=1
         AND RN >= {from_num}
         AND RN <= {to_num}
    '''.format(
      source=SOURCE_SQL,
      sorting=",".join(sorting),
      columns=",".join(column_names),
      from_num=from_num,
      to_num=to_num
    )

    # Execute DML
    res = self.executeQuery(PAING_SQL, sel_values)

    if dump:
      return self.loads(res).dumps()
    else:
      return res
  
  # For List Model
  def setPagination(self, source, **kwargs):
    pass

  # For list model
  def setPageInfo(self, *args, **kwargs):
    page = kwargs.get("page") or self.Meta.page_info.get("page") or self.Meta.page_info.get("first_page", 1)

    rows_per_page = kwargs.get("rows_per_page") or self.Meta.page_info.get("rows_per_page", 10)
    count_per_page = kwargs.get("count_per_page") or self.Meta.page_info.get("count_per_page", 10)
    
    total_count = kwargs.get("total_count") or self.Meta.page_info.get("total_count") or 0
    first_page = self.Meta.page_info.get("first_page")
    last_page = int(total_count / rows_per_page) + ( 1 if total_count % rows_per_page > 0 else 0 )

    start_page = int( page / count_per_page ) if int( page / count_per_page ) > 0 else first_page
    end_page = start_page + count_per_page - 1
    
    page = ( ( page if page < last_page else last_page ) if page > first_page else first_page )
    next_page = ( page + 1 ) if page < last_page else last_page
    prev_page = ( page - 1 ) if page > first_page else 1

    self.Meta.page_info.update(
      page=page,
      rows_per_page=rows_per_page,
      count_per_page=count_per_page,
      first_page=first_page,
      last_page=last_page,
      start_page=start_page,
      end_page=end_page,
      next_page=next_page,
      prev_page=prev_page,
      total_count=total_count,
      has_next_page=page < last_page,
      has_prev_page=page > first_page
    )