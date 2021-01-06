from app.database.connectors.sqlite import SQLiteConnector
from app.models.base import DatabaseModel
from app.utils.fields import (
  StringField,
  IntegerField,
  ListField,
  PickleField,
  DatetimeField
)

class SQLiteModel(DatabaseModel):
  def __init__(self, *args, **kwargs):
    self.Meta.db = SQLiteConnector()
    super(SQLiteModel, self).__init__(*args, **kwargs)


class SchedListModel(SQLiteModel):
  class Meta:
    table = "APSCHEDULER_JOBS"
    init = ["getDatas"]

  id = StringField(alias="id")
  next_run_time = StringField(alias="nextRunTime")
  job_state = PickleField(alias="jobState")


class LottoAPIModel(SQLiteModel):
  class Meta:
    table = "IF_LOTTO_PRZWIN_MST"
    init = []

  # Default Columns
  DRWT_NO             = IntegerField(alias="drwNo", PK=True, min=1)
  DRWT_NO_DATE        = StringField(alias="drwNoDate")
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
  
  # Extend Columns
  NEXT_DRWT_NO        = IntegerField(1, alias="nextDrwtNo", ignore=True, default_value="getNextDrwtNo")

  # Default Methods
  def getNotDttm(self, colname, info):
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

  def getUserName(self, colname, info):
    return "admin"

  # Custom Methods For Columns
  def getNextDrwtNo(self, colname, info):
    ''' TODO: Call the Method loads in parent class, throws only SQL and values '''

    retval = self.executeQuery('''
    SELECT IFNULL(MAX(DRWT_NO), 0)+1 AS NEXT_DRWT_NO 
      FROM IF_LOTTO_PRZWIN_MST
    ''', fetchone=True)

    if len(res) > 0:
      return res.pop()

    return None



class ListModel(SQLiteModel):
  class Meta:
    table = "IF_LOTTO_PRZWIN_MST"
    init = []
    limit = 2

  # Default Columns
  DRWT_NO             = IntegerField(alias="drwNo", min=1)
  DRWT_NO_DATE        = StringField(alias="drwNoDate")
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
  

class CustomListModel(SQLiteModel):
  # class Meta:
  #   table = "IF_LOTTO_PRZWIN_MST"
  
  lottoList = ListField(model=LottoAPIModel, countForPage=1)

  def get_lottoList(self, model, info):
    # Options
    countForPage = info.getOption("countForPage", 10)

    # Query Results
    res = model.executeQuery('''
    SELECT *
      FROM IF_LOTTO_PRZWIN_MST
     WHERE 1=1
     ORDER BY DRWT_NO DESC
     LIMIT %d
    ''' % ( countForPage ) )

    # Set Datas
    datas = list()
    for idx, data in enumerate(res):
      datas.append( model.load(data).dump() )

    return datas