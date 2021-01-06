import pytest

from app.database.models import CustomListModel

@pytest.mark.skip
def TestListModel():
  listModel = CustomListModel()
  print( listModel )

