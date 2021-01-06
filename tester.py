from app.database.connectors import SQLiteConnector
from app.database.models import SQLiteModel, ListModel, LottoAPIModel, SchedListModel

from tests.test_app import create_app
from tests.test_sched import TestLottoCrawlJob
from tests.test_orm import TestListModel

SQLiteConnector.init(db="./app/database/example.db")

# class IterApp:
#   def __init__(self, datas):
#     self.__datas = datas
#     self.__seek = 0
#     self.__start = 0
#     self.__end = len(datas)-1

#   def __iter__(self):
#     return self

#   def __next__(self):
#     if self.__seek <= self.__end:
#       data = self.__datas[self.__seek]
#       self.__seek += 1
#       return data
#     else:
#       raise StopIteration

# iter = IterApp([
#   'a', 'b', 'c', 'd'
# ])

# for data in iter:
#   print( data )

def test():
  
  TestLottoCrawlJob()

  model = SchedListModel()

  import pickle
  obj = model.dumps()[0].get("jobState")

  print( model.dumps() )

  #   a = [{'DRWT_NO': 1, 'drwtNo1': 10, 'drwtNo2': 23, 'drwtNo3': 29, 'drwtNo4': 33, 'drwtNo5': 37, 'drwtNo6': 40, 'bnusNo': 16, 'drwNoDate': '2002-12-07', 'firstAccumamnt': 863604600, 'firstWinamnt': 0, 'firstPrzwnerCo': 0, 'regDttm': '20201230232226', 'regUser': 'admin', 'returnValue': 'success', 'updDttm': '20201230232226', 'updUser': 'admin', '_BaseModel__datas': None, '_BaseModel__end': None, '_BaseModel__seek': None, '_BaseModel__start': None}, {'drwNo': 2, 'drwtNo1': 9, 'drwtNo2': 13, 'drwtNo3': 21, 'drwtNo4': 25, 'drwtNo5': 32, 'drwtNo6': 42, 'bnusNo': 2, 'drwNoDate': '2002-12-14', 'firstAccumamnt': 0, 'firstWinamnt': 2002006800, 'firstPrzwnerCo': 1, 'regDttm': '20201230232302', 'regUser': 
  # 'admin', 'returnValue': 'success', 'updDttm': '20201230232302', 'updUser': 'admin', '_BaseModel__datas': None, '_BaseModel__end': None, '_BaseModel__seek': None, '_BaseModel__start': None}]

  #   model = ListModel()
  #   datas = model.loads(a).dumps()
  #   print( datas )

  #   model2 = LottoAPIModel()
  #   print( model2.dump() )

  # model.getNextPage()
  # print( model.__datas )

  # for data in model:
    # print( data )
  

  # for data in model:
    # print( data )
  # print( model )
  # TestListModel()

  # app = create_app()
  # app.run("0.0.0.0", port=3001)
  
if __name__ == "__main__":
  test()
