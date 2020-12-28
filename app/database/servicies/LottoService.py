from app.database.models import LottoModel

class LottoService(LottoModel):
  def getNextPage(self, page=1, countForPage=10):
    return self.getPageLotto(page+1, countForPage)

  def getPrevPage(self, page=1, countForPage=10):
    return self.getPageLotto(page-1, countForPage)
