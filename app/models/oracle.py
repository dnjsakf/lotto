
from app.database.connectors.oracle import OracleConnector
from app.models.base import DatabaseModel
from app.utils.fields import (
  StringField,
  IntegerField,
  ListField,
  DatetimeField
)

__all__ = [
  "OracleModel",
  "ScottEmpModel",
  "LottoApiModel",
  "LottoApiListModel",
  "LottoApiDataModel"
]

class OracleModel(DatabaseModel):
  def __init__(self, *args, **kwargs):
    self.Meta.db = OracleConnector()
    self.Meta.symbol = ":"
    super(OracleModel, self).__init__(*args, **kwargs)


class ScottEmpModel(OracleModel):
  class Meta:
    schema = "SCOTT"
    table = "EMP"

  EMPNO = IntegerField(alias="empNo", PK=True)
  ENAME = StringField(alias="ename")
  JOB = StringField(alias="job")
  MGR = IntegerField(alias="mgr")
  HIREDATE = DatetimeField(alias="hiredate")
  SAL = IntegerField(alias="sal")
  COMM = IntegerField(alias="comm")
  DEPTNO = IntegerField(alias="deptno")
  

class LottoApiModel(OracleModel):
  class Meta:
    schema = "LOTTO"
    table = "IF_LOTTO_PRZWIN_MST"

  DRWT_NO             = IntegerField(alias="drwNo", PK=True, min=1)
  DRWT_NO_DATE        = DatetimeField(alias="drwNoDate", format="%Y-%m-%d")
  DRWT_NO1            = IntegerField(alias="drwtNo1", min=1, max=45)
  DRWT_NO2            = IntegerField(alias="drwtNo2", min=1, max=45)
  DRWT_NO3            = IntegerField(alias="drwtNo3", min=1, max=45)
  DRWT_NO4            = IntegerField(alias="drwtNo4", min=1, max=45)
  DRWT_NO5            = IntegerField(alias="drwtNo5", min=1, max=45)
  DRWT_NO6            = IntegerField(alias="drwtNo6", min=1, max=45)
  DRWT_NO_BNUS        = IntegerField(alias="bnusNo", min=1, max=45)
  FRST_ACCUM_AMOUNT   = IntegerField(alias="firstAccumamnt")
  FRST_PRZWIN_AMOUNT  = IntegerField(alias="firstWinamnt")
  FRST_PRZWIN_CO      = IntegerField(alias="firstPrzwnerCo")
  RTN_VAL             = StringField(alias="returnValue")
  REG_USER            = StringField(alias="regUser", default_value=lambda colname, info:"admin")
  REG_DTTM            = StringField(alias="regDttm", maxlength=14, default_value="getNotDttm")
  UPD_USER            = StringField(alias="updUser", default_value="getUserName")
  UPD_DTTM            = StringField(alias="updDttm", maxlength=14, default_value="getNotDttm")
  

class LottoApiListModel(OracleModel):
  class Meta:
    schema = "LOTTO"
    table = "IF_LOTTO_PRZWIN_MST"
    page_info = dict(
      first_page=1,
      rows_per_page=10,
      count_per_page=10
    )

  DRWT_NO             = IntegerField(alias="drwNo", PK=True, min=1)
  DRWT_NO_DATE        = DatetimeField(alias="drwNoDate", format="%Y-%m-%d")
  DRWT_NO1            = IntegerField(alias="drwtNo1", min=1, max=45)
  DRWT_NO2            = IntegerField(alias="drwtNo2", min=1, max=45)
  DRWT_NO3            = IntegerField(alias="drwtNo3", min=1, max=45)
  DRWT_NO4            = IntegerField(alias="drwtNo4", min=1, max=45)
  DRWT_NO5            = IntegerField(alias="drwtNo5", min=1, max=45)
  DRWT_NO6            = IntegerField(alias="drwtNo6", min=1, max=45)
  DRWT_NO_BNUS        = IntegerField(alias="bnusNo", min=1, max=45)
  FRST_ACCUM_AMOUNT   = IntegerField(alias="firstAccumamnt")
  FRST_PRZWIN_AMOUNT  = IntegerField(alias="firstWinamnt")
  FRST_PRZWIN_CO      = IntegerField(alias="firstPrzwnerCo")
  RTN_VAL             = StringField(alias="returnValue")
  REG_USER            = StringField(alias="regUser", default_value=lambda colname, info:"admin")
  REG_DTTM            = StringField(alias="regDttm", maxlength=14, default_value="getNotDttm")
  UPD_USER            = StringField(alias="updUser", default_value="getUserName")
  UPD_DTTM            = StringField(alias="updDttm", maxlength=14, default_value="getNotDttm")

  # Customs
  TOTAL_COUNT         = IntegerField(alias="totalCount", default_value="getTotalCount", ignore=True)

  def getTotalCount(self, colname=None, info=None):
    retval = self.executeQuery('''
      SELECT COUNT(1) AS TOTAL_COUNT
        FROM LOTTO.IF_LOTTO_PRZWIN_MST T1
        WHERE 1=1
    ''', fetchone=True, record_to_dict=True)

    total_count = int(retval.get("TOTAL_COUNT"))

    self.setPageInfo(total_count=total_count)

    return total_count

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

class LottoApiDataModel(OracleModel):
  
  nextDrwtNo = IntegerField(default_value="getNextDrwtNo")

  def getNextDrwtNo(self, colname, info):
    query = '''
      SELECT NVL(MAX(T1.DRWT_NO), 0)+1 AS %s
        FROM LOTTO.IF_LOTTO_PRZWIN_MST T1
        WHERE 1=1
    ''' % ( colname )

    retval = self.executeQuery(query, fetchone=True, record_to_dict=True)

    return retval.get( colname.upper() )
