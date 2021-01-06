import urllib
import json
  
def request(url, params=None):

  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
  }

  data = None
  if params is not None:
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')

  reqt = urllib.request.Request(url, data, headers)
  resp = urllib.request.urlopen(reqt)

  if resp.status == 200:
    return json.loads(resp.read())

  return None

resp = request("https://www.dhlottery.co.kr/common.do", params={
  "method": "getLottoNumber",
  "drwNo": nextDrwtNo
})

model.loads( resp )