from app.scheduler.builders import ScheduledBuilder

__all__ = [
  "BaseJob"
]

class BaseJob(object):
  def __init__(self, *args, **kwargs):
    self.name = self.__class__.__name__

    for key, val in kwargs.items():
      setattr(self, key, val)
      
  def build(self, **kwargs):
    execute = None
    schedule_type = None
    jobOptions = { "id": self.name }
    jobOptions.update(dict(kwargs))

    trigger = None
    triggerBuilder = None
    triggerOptions = dict()
    
    if hasattr(self, "execute"):
      execute = getattr(self, "execute")
      
    if hasattr(self, "schedule_type"):
      schedule_type = getattr(self, "schedule_type")
      triggerBuilder = ScheduledBuilder.getBuilder(schedule_type)

    for attrName in dir(self):
      if attrName in ("execute", "schedule_type"):
        continue

      attrValue = getattr(self, attrName)
      if attrName in triggerBuilder.__slots__:
        triggerOptions[attrName] = attrValue
      elif not callable(attrValue) and not attrName.startswith("__"):
        attrName = attrName if attrName != "name" else "id"
        jobOptions[attrName] = attrValue

    trigger = triggerBuilder.build(triggerOptions)
    
    return ( execute, trigger, jobOptions )

