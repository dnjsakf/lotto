
from datetime import datetime, timedelta

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
  "JobListModel",
  "JobSchedListModel",
  "JobSchedDateListModel",
]

class OracleModel(DatabaseModel):
  def __init__(self, *args, **kwargs):
    self.Meta.db = OracleConnector()
    self.Meta.symbol = ":"
    super(OracleModel, self).__init__(*args, **kwargs)
  
  REG_USER            = StringField(alias="regUser", default_value="admin")
  REG_DTTM            = StringField(alias="regDttm", maxlength=14, default_value=lambda c,i:datetime.now().strftime("%Y%m%d%H%M%S"))
  UPD_USER            = StringField(alias="updUser", default_value="admin")
  UPD_DTTM            = StringField(alias="updDttm", maxlength=14, default_value=lambda c,i:datetime.now().strftime("%Y%m%d%H%M%S"))


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

  
class JobListModel(OracleModel):
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

  JOB_ID              = StringField(alias="jobId", PK=True)
  JOB_NAME            = StringField(alias="jobName")

  
class JobSchedListModel(OracleModel):
  class Meta:
    schema = "LOTTO"
    table = "MT_JOB_SCHE_MST"
    page_info = dict(
      page=1,
      first_page=1,
      rows_per_page=10,
      count_per_page=10
    )
    description = dict()

  SCH_ID              = StringField(alias="schId", PK=True, default_value="getNextSchId")
  JOB_ID              = StringField(alias="jobId", PK=True)
  SCH_TYPE            = StringField(alias="schType")
  RUN_FLAG            = StringField(alias="runFlag", default_value="Y")
  LAST_RUN_DATE       = StringField(alias="lastRunDate")
  LAST_RUN_TIME       = StringField(alias="lastRunTime")

  def getNextSchId(self, colname, info):    
    return self.executeFunc("LOTTO.GET_NEXT_ID", str, ["SCH", self.Meta.table])

class JobSchedDateListModel(OracleModel):
  class Meta:
    schema = "LOTTO"
    table = "MT_JOB_SCHE_DATE_MST"
    page_info = dict(
      page=1,
      first_page=1,
      rows_per_page=10,
      count_per_page=10
    )
    description = dict()

  SCH_ID              = StringField(alias="schId", PK=True)
  JOB_ID              = StringField(alias="jobId", PK=True)
  RUN_DATE            = StringField(alias="runDate")
  RUN_TIME            = StringField(alias="runTime")
  RUN_DTTM            = StringField(alias="runDttm", default_value="getRunDttm")
  RUN_FLAG            = StringField(alias="runFlag", default_value="Y")

  def getRunDttm(self, colname, info):
    run_date = self.get("runDate", None)
    run_time = self.get("runTime", None)

    if run_date is not None and run_time is not None:
      run_date = run_date.replace("-", "")
      run_time = run_time.replace(":", "")
      return run_date+run_time

    return None
  
  