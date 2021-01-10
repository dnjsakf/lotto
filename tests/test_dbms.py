from pprint import pprint
from datetime import datetime

from app.database.connectors import SQLiteConnector,  OracleConnector
from app.models.sqlite import LottoAPIModel
from app.models.oracle import LottoJobListModel

SQLiteConnector.init(db="./app/database/example.db")
OracleConnector.init(db="CAMPDB", username="SYSTEM", password="campmaxquad12")

# data = dict(zip(['COMM', 'DEPTNO', 'EMPNO', 'ENAME', 'HIREDATE', 'JOB', 'MGR', 'SAL'], (None, None, 1000, None, datetime(2021, 1, 6, 14, 41, 39, 536233), None, None, None)))
# connector = OracleConnector()
# conn = connector.getConnection()
# cursor = conn.cursor()
# cursor.execute('''
#   INSERT INTO SCOTT.EMP (COMM, DEPTNO, EMPNO, ENAME, HIREDATE, JOB, MGR, SAL) VALUES (:COMM, :DEPTNO, :EMPNO, :ENAME, :HIREDATE, :JOB, :MGR, :SAL)
#   ''', dict(zip(['COMM', 'DEPTNO', 'EMPNO', 'ENAME', 'HIREDATE', 'JOB', 'MGR', 'SAL'], (None, None, 1000, None, datetime(2021, 1, 6, 14, 41, 39, 536233), None, None, None))))

# # for record in cursor.fetchall():
# #   print( record )
# conn.rollback()

# from app.utils.fields import StringField, IntegerField, ListField, DatetimeField

# from app.models.oracle import ScottEmpModel, LottoApiModel, LottoApiDataModel

# lottoApi = LottoApiModel()
# lottoApi.loads(lottoApi.getDatas())

# lottoApiData = LottoApiDataModel()
# print( lottoApi.dumps() )
# print( lottoApiData.dump() )

# model = ScottEmpModel(empNo=1000, hiredate=datetime.now())
# pprint( model.dump() )
# model.merge()

# listModel = CustomListModel()
# pprint( listModel.dump() )


# datas = [{'drwNo': 1, 'drwtNo1': 10, 'drwtNo2': 23, 'drwtNo3': 29, 'drwtNo4': 33, 'drwtNo5': 37, 'drwtNo6': 40, 'bnusNo': 16, 'drwNoDate': '2002-12-07', 'firstAccumamnt': 863604600, 'firstWinamnt': 0, 'firstPrzwnerCo': 0, 'returnValue': 'success'}, {'drwNo': 2, 'drwtNo1': 9, 'drwtNo2': 13, 'drwtNo3': 21, 'drwtNo4': 25, 'drwtNo5': 32, 'drwtNo6': 42, 'bnusNo': 2, 'drwNoDate': '2002-12-14', 'firstAccumamnt': 0, 'firstWinamnt': 2002006800, 'firstPrzwnerCo': 1, 'returnValue': 'success'}]
# model = ListModel()
# pprint( model.dumps() )

# from app.scheduler.launchers import JobLauncher
# from app.scheduler.jobs import LottoCrawlJob

# job = LottoCrawlJob()
# job.execute()

# testLauncher = JobLauncher(background=False)
# lottoCrawlJob = LottoCrawlJob(
#   name="tester",
#   schedule_type="interval",
#   minutes=1
# )
# testLauncher.addJob(lottoCrawlJob, args=["1", "2"], kwargs={"test": 10})
# testLauncher.start()


model = LottoJobListModel([
  {"jobId": "DumpCrawler1", "jobName": "DumpCrawler", "regUser": "admin", "regDttm": "20210101120000" },
  {"jobId": "DumpCrawler2", "jobName": "DumpCrawler", "regUser": "admin", "regDttm": "20210101120000" },
  {"jobId": "DumpCrawler3", "jobName": "DumpCrawler", "regUser": "admin", "regDttm": "20210101120000" },
  {"jobId": "DumpCrawler4", "jobName": "DumpCrawler", "regUser": "admin", "regDttm": "20210101120000" }
])
print( model.dumps() )

model.insertMany()