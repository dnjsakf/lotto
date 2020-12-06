from app.utils.database.connectors import SQLiteConnector

sqlite = SQLiteConnector("./datas/example.db")
sqlite.initLoadData(filename="./datas/lotto_1-940.xlsx")
sqlite.getLast()