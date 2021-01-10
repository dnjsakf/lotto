
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
  "LottoApiDataModel",
  "LottoJobListModel"
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
      page=1,
      first_page=1,
      rows_per_page=10,
      count_per_page=10
    )
    description = dict()

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
  

class LottoJobListModel(OracleModel):
  class Meta:
    schema = "LOTTO"
    table = "MT_JOB_MST"
    page_info = dict(
      page=1,
      first_page=1,
      rows_per_page=10,
      count_per_page=10
    )
    description = dict()

  JOB_ID              = IntegerField(alias="jobId", PK=True)
  JOB_NAME            = StringField(alias="jobName")
  REG_USER            = StringField(alias="regUser", default_value=lambda colname, info:"admin")
  REG_DTTM            = StringField(alias="regDttm", maxlength=14, default_value="getNotDttm")
  UPD_USER            = StringField(alias="updUser", default_value="getUserName")
  UPD_DTTM            = StringField(alias="updDttm", maxlength=14, default_value="getNotDttm")


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
