
import pytest
import traceback
from datetime import datetime, timedelta

from pprint import pprint
from typing import (
  Optional, Union, Any, Callable, Iterable, List, Dict, Tuple
)

from app.database.connectors import OracleConnection, OracleConnector

class BaseField(object):
  def __init__(
      self,
      valtype:Any,
      name:str=None,
      required:Optional[bool]=False,
      # default_value:Union[Callable,str]=None,
      **kwargs):

    self.__value = None
    self.__type = valtype
    self.__name = name
    self.__options = dict(kwargs)
    self.__required = required
  
  # 값 설정
  def setValue(self, value:Any, validate:Optional[bool]=True):
    self.__value = None
    
    if validate:
      # 값이 있는 경우 타입체크
      if value is not None and not isinstance(value, self.__type):
        raise TypeError("Expacted data type '%s', but '%s'." %( self.__type.__name__, value.__class__.__name__ ))
      
      # 유효성검사
      self.validate(value)
    
    self.__value = value

  def getType(self):
    return self.__type

  def getName(self):
    return self.__name
    
  def getValue(self):
    return self.__value
    
  def getOption(self, optkey, defaultvalue=None):
    return self.__options.get(optkey, defaultvalue)

  @property
  def required(self):
    return self.__required
  
  # Override
  def validate(self, value=None):
    pass
  
  def __str__(self):
    return str(self.__value)
    

# 문자열 필드
class StringField(BaseField):
  def __init__(
      self,
      maxlength:Optional[int]=None, 
      **kwargs):
      
    super(StringField, self).__init__(str, **kwargs)
    
    # 유효성검사 옵션값
    self.__maxlength = maxlength
  
  # Override: 유효성검사
  def validate(self, value=None):
    exists = value is not None
    value = value if exists else self.getValue()
    length = len(value) if exists else 0
    messages = self.getOption("messages", dict())
    
    # 유효성검사: 필수값
    if bool(self.required) and not exists:
      msg = "This value was Required, but it is None."
      msg = messages.get("required", msg)
      raise ValueError(msg)
    
    # 유효성검사: 최대길이
    if bool(self.__maxlength) and exists and length > self.__maxlength:
      msg = "Expacted value length %d, but %d." % ( self.__maxlength, length )
      msg = messages.get("maxlength", msg)
      raise ValueError(msg)

# 정수형 필드
class IntegerField(BaseField):
  def __init__(
      self,
      min:Optional[int]=None,
      max:Optional[int]=None,
      **kwargs):
    
    super(IntegerField, self).__init__(int, **kwargs)

    # 유효성검사 옵션값
    self.__min = min
    self.__max = max
  
  # Override: 유효성검사
  def validate(self, value=None):
    exists = value is not None
    value = value if exists else self.getValue()
    messages = self.getOption("messages", dict())
    
    # 유효성검사: 필수값
    if bool(self.required) and not exists:
      msg = "This value was Required, but it is None."
      msg = messages.get("required", msg)
      raise ValueError(msg)
    
    # 유효성검사: 최소값
    if bool(self.__min) and exists and value < self.__min:
      msg = "Expacted minimum %d, but %d." % ( self.__min, value )
      msg = messages.get("min", msg)
      raise ValueError(msg)

    # 유효성검사: 최댓값
    if bool(self.__max) and exists and value > self.__max:
      msg = "Expacted maximum %d, but %d." % ( self.__max, value )
      msg = messages.get("max", msg)
      raise ValueError(msg)

# 날짜형 필드
class DatetimeField(BaseField):
  def __init__(
      self,
      format:str="%Y-%m-%d %H:%M:%S",
      *args,
      **kwargs
      ):
    super(DatetimeField, self).__init__(datetime, *args, **kwargs)

    self.__value = None
    self.__format = format

  # 값 설정
  def setValue(self, value:Union[str,datetime], format:str=None, validate:Optional[bool]=True):
    # 값이 문자열인 경우, datetime으로 치환
    if isinstance(value, str):
      value = datetime.strptime(value, format or self.__format)

    self.__value = None
    
    if validate:
      # 값이 있는 경우 타입체크
      if value is not None and not isinstance(value, self.getType()):
        raise TypeError("Expacted data type '%s', but '%s'." %( self.getType().__name__, value.__class__.__name__ ))
      
      # 유효성검사
      self.validate(value)
    
    self.__value = value

  def getValue(self) -> datetime:
    return self.__value


# 기본 데이터 모델
class BaseModel(object):
  def __init__(
      self,
      data:Optional[Union[dict,Iterable]]=None,
      ignore:List=list(),
      **kwargs
      ):
    
    self.__datas = None
    self.__seek = 0
    self.__size = 0
    self.__errors = None
    self.__ignore = ignore
    
    # Init Dumpping
    if data is not None:
      self.dumps(data)

  # Snake String to Camelcase String
  def snake_to_camel(self, snake):
    init, *temp = snake.split('_') 
    return''.join([init.lower(), *map(str.title, temp)])  

  # 필드명, 필드클래스 가져오기
  #   @PK: 필드 옵션 중 PK를 비교
  #   @ignore: 제외 컬럼 목록
  def getFields(self, PK=None, ignore:List=None) -> List:
    fields = list()
    for field_name in dir(self):
      # 컬럼명, 컬럼필드 저장
      field_class = getattr(self, field_name)

      if not callable(field_class) and not field_name.startswith("_"):
        # 무시할 컬럼 설정
        if bool(ignore) and field_name in self.getIgnore(ignore):
          continue
        
        if isinstance(field_class, BaseField):
          # PK만 조회하는 경우
          if PK is not None and PK != bool(field_class.getOption("PK")):
            continue

          fields.append((field_name, field_class))

    return fields

  # 필드에 저장된 데이터 가져오기
  def getData(self, index:int=0, ignore:List=None) -> Dict:
    return self.load(self.__datas[index], ignore=ignore)

  # 데이터 목록 가져오기
  def getDatas(self, ignore:List=None) -> List:
    return self.loads(self.__datas, ignore=ignore)
  
  # 데이터 사이즈 가져오기
  def getSize(self) -> int:
    return self.__size

  # 제외할 컬럼 목록 가져오기
  def getIgnore(self, ignore:List=None) -> List:
    return ignore or self.__ignore

  # 값만 매핑
  def dump(self, data:dict, ignore:List=None) -> Dict:
    self.precheck(data, Dict)
    
    fields = self.getFields(ignore=ignore)
    dumped = dict()

    for field_name, field_class in fields:
      key = field_name
      field_class.setValue(data.get(key, None), validate=False)
      value = field_class.getValue()

      if key is not None:
        dumped[key] = value

    return dumped

  # 값을 매핑 && 유효성검사
  def load(self, data:Dict, ignore:List=None, errors=False) -> Dict:
    self.precheck(data, Dict)

    # 유효하지않은 값은 __errors에 저장하여 반환
    self.__errors = list()

    fields = self.getFields(ignore=ignore)
    loaded = dict()

    for field_name, field_class in fields:
      try:
        # key = self.snake_to_camel() if camel else field_name
        key = field_name
        field_class.setValue(data.get(key, None))
        value = field_class.getValue()

        # 기본값 설정
        default_value = field_class.getOption("default_value")

        if key not in data and default_value is not None:
          key = field_name
          if callable(default_value):
            value = default_value(field_class)
          elif hasattr(self, default_value) and callable(getattr(self, default_value)):
            value = getattr(self, default_value)(field_class)
          else:
            value = default_value

          loaded[key] = value
        
        elif key in data:
          loaded[key] = value
        
      except Exception as e:
        self.__errors.append((field_name, str(e)))

    if errors:
      loaded.update(__errors=dict(self.__errors))

    return loaded
    
  # Dupping
  def dumps(self, datas:List, ignore:List=None) -> List:
    res_datas = list()
    if isinstance(datas, Dict):
      res_datas.append(self.dump(datas, ignore=ignore))
    else:
      for data in datas:
        res_datas.append(self.dump(data, ignore=ignore))
      
    self.__datas = res_datas
    self.__seek = 0
    self.__size = len(res_datas)
    
    return res_datas
  
  # Loadding
  def loads(self, datas:Iterable, ignore:List=None, errors=False) -> List:
    res_datas = list()
    if isinstance(datas, Dict):
      res_datas.append(self.load(datas, ignore=ignore, errors=errors))
    else:
      for data in datas:
        res_datas.append(self.load(data, ignore=ignore, errors=errors))
      
    self.__datas = res_datas
    self.__seek = 0
    self.__size = len(res_datas)
      
    return res_datas

  def precheck(self, data:Any, datatype:Any):
    if data is None:
      raise ValueError("Expected list type value, but value is None.")
    if not isinstance(data, datatype):
      raise TypeError("Expected %s type, but %s" % ( self.getType().__name__,  data.__class__.__name__ ))

  def __str__(self):
    return str(self.getDatas())
    
  def __iter__(self):
    return self
    
  def __next__(self):
    if self.__seek < self.__size:
      data = self.getData(self.__seek)
      self.__seek += 1
      return data
    else:
      raise StopIteration


OracleConnector.init(**dict(
  username="SYSTEM",
  password="campmaxquad12",
  db="CAMPDB",
  url="localhost",
  port=1521
))

# Database(ORACLE)형 데이터 모델
class DatabaseModel(BaseModel):
  # Database META
  class Meta:
    pass

  __meta_slots__ = [
    ("db", None),
    ("schema", None),
    ("table", None),
    ("symbol", ":"),
    ("page_info", dict()),
    ("description", None)
  ]

  __set_mapp__ = dict(
    SET=("=", True)
  )

  __where_mapp__ = dict(
    EQ=("=", True),
    NE=("!=", True),
    LE=("<=", True),
    GE=(">=", True),
    LT=("<", True),
    GT=(">", True),
    IN=("IN", True),
    NOTIN=("NOT IN", True),
    LIKE=("LIKE", True),
    NOTLIKE=("NOT LIKE", True),
    NULL=("IS NULL", False),
    NOTNULL=("IS NOT NULL", False)
  )

  __order_mapp__ = dict(
    ASC=("ASC", False),
    DESC=("DESC", False)
  )

  def __init__(
      self,
      datas:Union[Dict,List]=None,
      page_info:Dict=None,
      *args,
      **kwargs):

    # Meta Default Settings
    for slot_name, default_value in self.__meta_slots__:
      if not hasattr(self.Meta, slot_name):
        setattr(self.Meta, slot_name, default_value)
    
    # 필수값 체크
    if self.Meta.table is None:
      raise ValueError("Not found table, please define Meta.table.")

    # Database Connection 객체 생성
    self.Meta.db = OracleConnector()

    # 페이징 정보 초기 설정
    init_page_info = dict(page=1, rows_per_page=10)
    if page_info is not None:
      init_page_info.update(page_info)
    self.Meta.page_info.update(init_page_info)
    self.setPageInfo()

    super(DatabaseModel, self).__init__(datas, *args, **kwargs)

  # 테이블명 가져오기(With. 스키마)
  def getTableName(self) -> str:
    return (self.Meta.schema+"." if self.Meta.schema else "")+self.Meta.table
  
  # 컬럼 목록 가져오기
  def getColumns(self, PK=None, ignore:List=None) -> List:
    cols = list()
    for field_name, field_class in self.getFields(PK=PK, ignore=ignore):
      cols.append(field_name)
    return cols

  # Operation 빌드
  def __build_operation(self, options:Dict):
    where = list()
    values = list()
    order = list()

    for key, value in options.items():
      colname, opertype = key.split("__")

      if opertype in self.__where_mapp__:
        # WHERE 절
        operator, save = self.__where_mapp__.get(opertype, (None, None))
        if operator is not None:
          cond = "AND " + colname + " " + operator

          # 값을 저장하는 조건
          if save:
            if operator in ("IN", "NOT IN"):
              temp = " ("
              for idx, invalue in enumerate(value):
                if idx != 0:
                  temp += ","
                temp += self.Meta.symbol+colname+str(idx+1)
                values.append(invalue)
              temp += ")"

              where.append(cond + temp)
              
            else:
              where.append(cond + " " + self.Meta.symbol+colname)
              values.append(value)

          # 값을 저장하지 않는 조건(IS NULL, IS NOT NULL)
          else:
            where.append(cond)

      elif opertype in self.__order_mapp__:
        # ORDER BY 절
        operator, save = self.__order_mapp__.get(opertype, (None, None))
        
        if value and operator is not None:
          order.append(colname+" "+operator)

      elif opertype in self.__set_mapp__:
        # UPDATE / SET 절
        operator, save = self.__set_mapp__.get(opertype, (None, None))

      else:
        raise ValueError("Not suppoerted operator.")
          
    return ( where, values, order )

  # 데이터 저장(Insert)
  def insert(self, ignore:List=None) -> int:
    table = self.getTableName()
    columns = self.getColumns(ignore=ignore)
    pstmts = [ self.Meta.symbol+column for column in columns ]

    # Insert SQL
    SQL = '''
      INSERT INTO {table} ( {columns} ) VALUES ( {pstmts} )
    '''.format(
      table=table,
      columns=",".join(columns),
      pstmts=",".join(pstmts)
    )

    return self.Meta.db.executeMany(SQL, self.getDatas())

  # 데이터 삭제(Delete)
  def delete(self, **kwargs):
    table = self.getTableName()
    where, values, _ = self.__build_operation(kwargs)
    
    # Delete SQL
    SQL = '''
      DELETE FROM {table} WHERE 1=1 {where}
    '''.format(
      table=table,
      where=" ".join(where),
    )

    return self.Meta.db.executeUpdate(SQL, values)

  # 데이터 수정(Update)
  def update(self, **kwargs):

    table = self.getTableName()
    setter = list()
    values = list()

    for key, value in kwargs.items():
      colname, operator = key.split("__")
      if operator == "SET":
        setter.append(colname+" = "+self.Meta.symbol+colname)
        values.append(value)

    where, _values, _ = self.__build_operation(kwargs)
    
    # Update SQL
    SQL = '''
      UPDATE {table}
         SET {setter}
       WHERE 1=1 
         {where}
    '''.format(
      table=table,
      setter=", ".join(setter),
      where=" ".join(where),
    )

    print( SQL )

    return self.Meta.db.executeUpdate(SQL, values+_values)
  
  # 데이터 저장하기(Delete and Insert)
  def save(self, many=True, delete=True) -> int:
    
    deletecount = 0
    insertcount = 0
    updatecount = 0
  
    # PK 컬럼&데이터 조회
    PKs = list()
    SETs = list()

    for data in self.getDatas():
      print( data )
      for PK in self.getColumns(PK=True):
        PKs.append(dict([
          ( PK+"__EQ", data.get(PK) )
        ]))

      temp = dict()
      for SET in self.getColumns(PK=False):
        if not SET in data:
          continue

        temp[SET+"__SET"] = data.get(SET, None)

      SETs.append(temp)

    if delete:
      # PK 데이터 삭제
      for pk_columns in PKs:
        records = self.selectOne(**pk_columns)
        if records is not None:
          deletecount += self.delete(**pk_columns)
    
      # 데이터 입력
      insertcount = self.insert()

    else:
      # PK 데이터 삭제
      for pk_columns, set_columns in zip(PKs, SETs):
        pk_columns.update(set_columns)

        updatecount += self.update(**pk_columns)

    print("DELETED: %d" % ( deletecount ))
    print("UPDATED: %d" % ( updatecount ))
    print("INSERTED: %d" % ( insertcount ))

    return insertcount

  # 데이터 가져오기(Fetch One)
  def selectOne(self, ignore:List=None, **kwargs) -> Dict:
    '''
      DQL
        - 데이터 조회
    '''
    columns = self.getColumns(ignore=ignore)
    where, values, order = self.__build_operation(kwargs)
    
    SQL = '''
        SELECT {columns}
          FROM {table}
         WHERE 1=1
           {where}
    '''.format(
      columns=",".join(columns),
      table=self.getTableName(),
      where=" ".join(where)
    )
    if len(order) > 0:
      SQL += '''
         ORDER BY {order}
      '''.format(order=",".join(order))

    print( SQL )
    
    record = self.Meta.db.executeQuery(SQL, values, fetchone=True)
    if record is not None:
      return self.load(record, ignore=ignore)
    return None


  # 데이터 목록 가져오기(Fetch All)
  def select(self, ignore:List=None, **kwargs) -> List:
    '''
      DQL
        - 데이터 목록 조회
    '''
    columns = self.getColumns(ignore=ignore)
    where, values, order = self.__build_operation(kwargs)

    from_num = (self.Meta.page_info.get("rows_per_page") * ( self.Meta.page_info.get("page") - 1 )) + 1
    to_num = self.Meta.page_info.get("rows_per_page") * self.Meta.page_info.get("page")

    # Main SQL
    SOURCE_SQL = '''
        SELECT {columns}
          FROM {table}
         WHERE 1=1
           {where}
    '''.format(
      columns=",".join(columns),
      table=self.getTableName(),
      where=" ".join(where)
    )
    if len(order) > 0:
      SOURCE_SQL += '''
         ORDER BY {order}
      '''.format(order=",".join(order))

    # Page Info SQL
    TOTAL_SQL = '''
    WITH TOTAL_OBJ AS (
      {source}
    )
    SELECT COUNT(1) AS TOTAL_COUNT
      FROM TOTAL_OBJ
    '''.format(
      source=SOURCE_SQL
    )
    records = self.Meta.db.executeQuery(TOTAL_SQL, values, fetchone=True)

    self.setPageInfo(total_count=records.get("TOTAL_COUNT"))

    # Page Data SQL
    if len(order) == 0:
      order.append(columns[0]+" ASC")

    PAING_SQL = '''
      WITH SOURCE_OBJ AS (
        {source}
      ), SORT_OBJ AS (
        SELECT {columns}
             , ROW_NUMBER() OVER( ORDER BY {order} ) AS RN
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
      columns=",".join(columns),
      order=",".join(order),
      from_num=from_num,
      to_num=to_num
    )

    records = self.Meta.db.executeQuery(PAING_SQL, values)
    
    return self.loads(records, ignore=ignore)
    
  def setPageInfo(self, *args, **kwargs):
    current_page = kwargs.get("current_page") or self.Meta.page_info.get("current_page") or self.Meta.page_info.get("first_page", 1)
    page = kwargs.get("page") or self.Meta.page_info.get("page") or current_page
    
    rows_per_page = kwargs.get("rows_per_page") or self.Meta.page_info.get("rows_per_page", 10)
    count_per_page = kwargs.get("count_per_page") or self.Meta.page_info.get("count_per_page", 10)

    total_count = kwargs.get("total_count") or self.Meta.page_info.get("total_count") or 0
    first_page = self.Meta.page_info.get("first_page") or 1
    last_page = int(total_count / rows_per_page) + ( 1 if total_count % rows_per_page > 0 else first_page )

    start_page = int( current_page / count_per_page ) if int( current_page / count_per_page ) > 0 else first_page
    end_page = start_page + count_per_page - 1
    
    current_page = ( ( current_page if current_page < last_page else last_page ) if current_page > first_page else first_page )
    next_page = ( current_page + 1 ) if current_page < last_page else last_page
    prev_page = ( current_page - 1 ) if current_page > first_page else 1

    self.Meta.page_info.update(
      page=page,                      # 현재 페이지(입력한 페이지)
      current_page=current_page,      # 현재 페이지(유효한 페이지)
      rows_per_page=rows_per_page,    # 노출 목록수
      count_per_page=count_per_page,  # 노출 페이지수
      first_page=first_page,          # 첫 페이지
      last_page=last_page,            # 끝 페이지
      start_page=start_page,          # 노출 페이지수 기준 첫 페이지
      end_page=end_page,              # 노출 페이지수 기준 끝 페이지
      prev_page=prev_page,            # 이전 페이지
      next_page=next_page,            # 다음 페이지
      has_prev_page=page > first_page,# 이전 페이지 여부
      has_next_page=page < last_page, # 다음 페이지 여부
      total_count=total_count         # 전체 목록수
    )

class DummyModel(BaseModel):
  id = StringField(name="ID", required=True, maxlength=10)
  name = StringField(name="NAME", maxlength=10)
  
class DummyBaseModel(BaseModel):
  id = StringField(name="ID", required=True, maxlength=10)
  name = StringField(name="NAME", required=True, maxlength=10, messages=dict(required="a"))
  seq = IntegerField(name="SEQ", min=10, max=15)

class DummyDBModel(DatabaseModel):
  class Meta:
    schema = "LOTTO"
    table = "IF_LOTTO_PRZWIN_MST"

  DRWT_NO	            = IntegerField(required=True, PK=True)
  DRWT_NO_DATE		    = DatetimeField()
  DRWT_NO1            = IntegerField(min=1,max=45)
  DRWT_NO2            = IntegerField(min=1,max=45)
  DRWT_NO3            = IntegerField(min=1,max=45)
  DRWT_NO4            = IntegerField(min=1,max=45)
  DRWT_NO5            = IntegerField(min=1,max=45)
  DRWT_NO6            = IntegerField(min=1,max=45)
  DRWT_NO_BNUS        = IntegerField(min=1,max=45)
  FRST_ACCUM_AMOUNT	  = IntegerField()
  FRST_PRZWIN_AMOUNT  = IntegerField()
  FRST_PRZWIN_CO      = IntegerField()
  RTN_VAL             = StringField(maxlength=500)
  REG_USER            = StringField(maxlength=50)
  REG_DTTM            = StringField(maxlength=14, default_value="getNow")
  UPD_USER            = StringField(maxlength=50)
  UPD_DTTM            = StringField(maxlength=14, default_value="getNow" )

  def getNow(self, info):
    return datetime.now().strftime("%Y%m%d%H%M%S")

@pytest.mark.skip
def test_StringField_1():
  print('============ test_StringField_1 - 1')
  field = StringField(required=True, maxlength=10)
  field.setValue("string")
  pprint( field.getValue() )

@pytest.mark.skip
def test_IntegerField_1():
  print('============ test_IntegerField_1 - 1')
  field = IntegerField(required=True, min=0, max=10)
  field.setValue(0)
  pprint( field.getValue() )

@pytest.mark.skip
def test_DatetimeField_1():
  print('============ DatetimeField - 1')
  field = DatetimeField()
  field.setValue("20210114000000", format="%Y%m%d%H%M%S")
  pprint( field )


@pytest.mark.skip
def test_DummyModel_1_init():
  print('============ DummyModel - 1')
  model = DummyModel({
    "name": "model1"
  })
  print( model )
    
@pytest.mark.skip
def test_DummyModel_2_dump():
  print('============ DummyModel - 2')
  model = DummyModel()
  data = model.dump({
    "name": "model2"
  })
  print( model )
  for key, value in data.items():
    pprint("%s=%s" % (key, value))
    
@pytest.mark.skip
def test_DummyModel_2_load():
  print('============ DummyModel - 3')
  model = DummyModel()
  data = model.load({
    "name": "model3"
  })
  print( model )
  for key, value in data.items():
    pprint("%s=%s" % (key, value))


@pytest.mark.skip
def test_DummyBaseModel_2_init():
  print('============ DummyBaseModel - 1')
  model = DummyBaseModel([
    {"id": "model1"},
    {"id": "model2"}
  ])
  print( model )
  for data in model:
    pprint( data )

@pytest.mark.skip
def test_DummyBaseModel_2_dumps():
  print('============ DummyBaseModel - 2')
  model = DummyBaseModel()
  model.dumps([
    {"id": "model1"},
    {"id": "model2"}
  ])
  print( model )
  for data in model:
    pprint( data )

@pytest.mark.skip
def test_DummyBaseModel_2_loads():
  print('============ DummyBaseModel - 3')
  model = DummyBaseModel()
  model.loads([
    {"id": "model1"},
    {"id": "model2"}
  ])
  print( model )
  for data in model:
    pprint( data )

@pytest.mark.skip
def test_DatabaseModel_1_DQL():
  print('============ DummyDBModel - 1')
  model1 = DummyDBModel(page_info=dict(
    rows_per_page=10,
    page=1
  ))
  records = model1.select(
    cond=dict(
      DRWT_NO__LT=3,
      FRST_PRZWIN_AMOUNT__NOTNULL=None,
    ),
    sort=[
      "DRWT_NO__DESC",
      "FRST_PRZWIN_AMOUNT__ASC"
    ]
  )
  pprint(records)

# @pytest.mark.skip
def test_DatabaseModel_2_DML_insert():
  print('============ DummyDBModel - 2')

  model = DummyDBModel()
  data = model.loads([{
      'DRWT_NO': -1,
      'DRWT_NO1': 1,
      'DRWT_NO2': 3,
      'DRWT_NO3': 4,
      'DRWT_NO4': 5,
      'DRWT_NO5': 1,
      'DRWT_NO6': 6,
      'DRWT_NO_BNUS': None
    }
    , {
      'DRWT_NO': 0,
      'DRWT_NO1': 10,
      'DRWT_NO2': 23,
      'DRWT_NO3': 29,
      'DRWT_NO4': 33,
      'DRWT_NO5': 37,
      'DRWT_NO6': 40,
      'DRWT_NO_BNUS': 16,
      'DRWT_NO_DATE': '2002-12-07 00:00:00',
      'FRST_ACCUM_AMOUNT': 863604600,
      'FRST_PRZWIN_AMOUNT': None,
      'FRST_PRZWIN_CO': None,
      'REG_DTTM': None,
      'REG_USER': 'admin',
      'RTN_VAL': 'success',
      'UPD_DTTM': None,
      'UPD_USER': None
    }
  ], errors=True)
  
  model.save(delete=False)
  
  # for data in model.select():
  #   pprint( data )

  # for item in model:
  #   pprint( item )

  # model.update(
  #   UPD_DTTM__SET="10",
  #   DRWT_NO__EQ=0
  # )
    
  # model.insert(many=True)
  # model.save(many=True)
  
  # DRWT_NO IN (1, 5, 9)
  # pprint( model.select(DRWT_NO__IN=[1, 5, 9]) )
  
  # DRWT_NO NOT IN (1, 5, 9)
  # pprint( model.select(DRWT_NO__NOTIN=[1, 5, 9]) )

  # for data in model.select(
  #     DRWT_NO__LE=3,
  #     REG_USER__LIKE="%min",
  #     DRWT_NO__DESC=True,
  #     REG_DTTM__ASC=False,
  #     ignore=[
  #       "REG_USER", "REG_DTTM", "UPD_USER", "UPD_DTTM"
  #     ]
  #   ):
  #   pprint(data)

  # pprint( model.selectOne(DRWT_NO__EQ=3) )

  # model.save()
  # data = model.loads([{
  #   'DRWT_NO': 0,
  #   'DRWT_NO1': 10,
  #   'DRWT_NO2': 23,
  #   'DRWT_NO3': 29,
  #   'DRWT_NO4': 33,
  #   'DRWT_NO5': 37,
  #   'DRWT_NO6': 40,
  #   'DRWT_NO_BNUS': 16,
  #   'DRWT_NO_DATE': '2002-12-07 00:00:00',
  #   'FRST_ACCUM_AMOUNT': 863604600,
  #   'FRST_PRZWIN_AMOUNT': None,
  #   'FRST_PRZWIN_CO': None,
  #   'REG_DTTM': None,
  #   'REG_USER': 'admin',
  #   'RTN_VAL': 'success',
  #   'UPD_DTTM': None,
  #   'UPD_USER': None
  # }])
  # model.save(many=True)

