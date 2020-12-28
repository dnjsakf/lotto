import pandas as pd

class PandasTimestampFormat(object):
  def __init__(self, datas):
    self.index = 0
    self.size = len(datas)
    self.datas = datas

  def __iter__(self):
    self.index = 0
    return self
  
  def __next__(self):
    if self.index >= self.size:
      raise StopIteration

    data = self.datas[self.index]

    if isinstance(data[1], pd._libs.tslibs.timestamps.Timestamp):
      data[1] = data[1].strftime('%Y%m%d%H%M%S')

    self.index += 1

    return data