import requests
import json

class BaseModel(object):
  def __init__(self, **kwargs):
    pass

  def loads(self, data=None):
    assert data is not None, "Data is None"
    for attrName in dir(self):
      attr = getattr(self, attrName)
      if not callable(attr) and not attrName.startswith("__"):
        if attrName in data:
          setattr(self, attrName, data.get(attrName, None))

  def __str__(self):
    attrs = list()
    for attrName in dir(self):
      attr = getattr(self, attrName)
      if not callable(attr) and not attrName.startswith("__"):
        attrs.append(( attrName, attr ))
    return str(attrs)

class IF_LOTTO_PRZWIN_MST(BaseModel):
  DRWT_NO = None
  DRWT_NO_DATE = None
  DRWT_NO1 = None
  DRWT_NO_DATE = None
  DRWT_NO1 = None
  DRWT_NO2 = None
  DRWT_NO3 = None
  DRWT_NO4 = None
  DRWT_NO5 = None
  DRWT_NO6 = None
  DRWT_NO_BNUS = None
  FRST_ACCUM_AMOUNT = None
  FRST_PRZWIN_AMOUNT = None
  FRST_PRZWIN_CO = None
  RTN_VAL = None
  REG_USER = None
  REG_DTTM = None
  UPD_USER = None
  UPD_DTTM = None

# req = requests.get("https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=903")
# if req.status_code == 200:
  # data = json.loads( req.text )

model = IF_LOTTO_PRZWIN_MST()
model.loads(data={
  "DRWT_NO": 1
})

print( model )