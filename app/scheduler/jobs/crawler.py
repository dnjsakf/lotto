import logging
import urllib
import json

from .base import BaseJob

from app.models.oracle import LottoApiModel, LottoApiDataModel


class LottoCrawlerJob(BaseJob):
  '''
    매주 토요일 저녁 9시 30분에 최신 추첨 정보 조회하는 크롤러
  '''
  name = "LottoCrawlerJob"
  schedule_type = "date"

  def execute(self, *args, **kwargs):
    print("===== Crawl Start =====")

    # 다음 회차 정보 가져오기
    model = LottoApiDataModel()
    datas = model.dump()
    nextDrwtNo = datas.get("nextDrwtNo", 1)

    response = self.__request("https://www.dhlottery.co.kr/common.do", {
      "method": "getLottoNumber",
      "drwNo": nextDrwtNo
    })

    responseData = None
    if response.status == 200:
      responseData = json.loads(response.read())

    print("responseData: %s" % ( responseData ))

    if responseData is not None:
      LottoApiModel(**responseData).merge()

    print("===== Crawl Finish =====")
    launcher = kwargs.get("launcher", None)
    if launcher is not None:
      launcher.removeJob(self.name)

  def __request(self, url, params=None):
    print("request: %s" % ( url ))
    print("params: %s" % ( params ))

    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')

    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    }

    request = urllib.request.Request(url, data, headers)
    response = urllib.request.urlopen(request)

    return response