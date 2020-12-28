from app.database.servicies import LottoService

service = LottoService("./app/database/example.db")




class FirstModel(object):

  db = "example.db"

  def __init__(self, db=None):
    pass

  @classmethod
  def init(cls, db=None):
    if db is not None:
      cls.db = db

class SecondModel(FirstModel):

  def printf(self):
    print( self.db )

FirstModel.init("init.db")
model = SecondModel()

print( model.db )