import pytest

from app.database.connectors import SQLiteConnector
from app.scheduler.launchers import JobLauncher

SQLiteConnector.init(db="./app/database/example.db")
 
@pytest.mark.skip
def TestLottoCrawlJob():
  from app.scheduler.launchers import JobLauncher
  from app.scheduler.jobs import LottoCrawlJob

  testLauncher = JobLauncher(background=True)
  lottoCrawlJob = LottoCrawlJob(
    name="tester",
    schedule_type="interval",
    seconds=10
  )
  testLauncher.addJob(lottoCrawlJob, args=["1", "2"], kwargs={"test": 10})
  testLauncher.start()

# print( model.dump() )
# datas = model.dump()

# listModel = LottoListModel()
# print( listModel.dump() )

# nextDrwtNo = datas.get("nextDrwtNo", 1)

# selected = model2.select()
# updated = model2.update()
# deleted = model.delete()
# inserted = model.insert()

# print( updated, deleted, inserted )
