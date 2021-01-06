import pickle
from datetime import datetime, timedelta

from typing import Optional, Union

class BaseField(object):
  
  value = None

  def __init__(self, value=None, _type=None, **kwargs):
    if value is not None:
      self.value = _type(value)

    self._type = _type
    self.option = kwargs

    valid, reason = self._validate()
    if not valid:
      print(reason)

  def __str__(self):
    return "[ value=%s ]" % ( self.value )
  
  def __name__(self):
    return self.__name__

  def getValue(self):
    return self.value

  def setValue(self, value=None):
    if value is not None:
      self.value = self._type(value)
      
  def setOption(self, key, value):
    self.option[key] = value

  def getOption(self, key, default_value=None):
    return self.option.get(key, default_value)

  def _validate(self):
    valid = True
    reason = "Success"
    
    required = bool(self.option.get("required"))
    try:
      if required:
        assert self.value is not None, "Value is Nodne."

      if self.value is not None:
        if not isinstance(self.value, self._type):
          raise Exception("Expected '%s' type, but '%s' type." % ( str(self._type.__name__), str(self.value.__class__.__name__) ))

      if hasattr(self, "validate"):
        valid, reason = self.validate()

    except Exception as e:
      valid = False
      reason = str(e)

    return valid, reason

class StringField(BaseField):
  def __init__(self, value=None, **kwargs):
    super(StringField, self).__init__(value, str, **kwargs)

  def validate(self):
    valid = True
    reason = "Success"

    try:
      if self.value is not None:
        maxlength = self.option.get("maxlength", 0)
        if maxlength > 0 and len(self.value) > maxlength:
          raise Exception("Max length is %d, but %d" % ( maxlength, len(self.value) ))

    except Exception as e:
      valid = False
      reason = str(e)

    return (valid, reason)


class IntegerField(BaseField):
  def __init__(self, value=None, **kwargs):
    super(IntegerField, self).__init__(value, int, **kwargs)

  def validate(self):
    valid = True
    reason = "Success"

    try:
      if self.value is not None:
        max = self.option.get("max", 0)
        min = self.option.get("min", 0)

        if max > 0 and self.value > max:
          raise Exception("Expected value grater than '%d', but value is '%d'." % ( max, self.value )) 
        
        if min > 0 and self.value < min:
          raise Exception("Expected value less than '%d', but value is '%d'." % ( min, self.value )) 

    except Exception as e:
      valid = False
      reason = str(e)

    return (valid, reason)


class ListField(BaseField):
  def __init__(self, value=None, **kwargs):
    super(ListField, self).__init__(value, list, **kwargs)

  def validate(self):
    valid = True
    reason = "Success"

    try:
      ''' TODO: Write validation logics for ListField '''

    except Exception as e:
      valid = False
      reason = str(e)

    return (valid, reason)


class PickleField(BaseField):
  def __init__(self, value=None, **kwargs):
    super(PickleField, self).__init__(value, dict, **kwargs)
  
  def setValue(self, value):
    if value is not None:
      self.value = pickle.loads(value)
    

class DatetimeField(BaseField):
  __default_format = "%Y-%m-%d %H:%M:%S"

  def __init__(self, value=None, **kwargs):
    super(DatetimeField, self).__init__(value, timedelta, **kwargs)

  def setValue(self, value):
    format = self.getOption("format", self.__default_format)
    if value is not None and isinstance(value, str):
      value = self.strptime(value, format)
    self.value = value

  def strftime(self, value:str, format=None):
    if format is None:
      format = self.getOption("format", self.__default_format)
    return datetime.strftime(value, format)

  def strptime(self, value:datetime, format=None):
    if format is None:
      format = self.getOption("format", self.__default_format)
    return datetime.strptime(value, format)
