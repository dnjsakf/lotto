from typing import Union

from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import AndTrigger, OrTrigger

__all__ = [
  "DateScheduledBuilder",
  "IntervalScheduledBuilder",
  "CronScheduledBuilder",
  "ScheduledBuilder"
]

# trigger = OrTrigger([CronTrigger(day_of_week='sat', hour=10),
#                      CronTrigger(day_of_week='tue', hour='3-5')])

class DateScheduledBuilder(object):

  __slots__ = ["run_date", "timezone"]
  
  @staticmethod
  def build(sched:dict) -> DateTrigger:
    sched.setdefault("run_date"   , None) # (datetime|str) – the date/time to run the job at
    sched.setdefault("timezone"   , None) # (datetime.tzinfo|str) – time zone for run_date if it doesn’t have one already
    return DateTrigger(**sched)


class IntervalScheduledBuilder(object):

  __slots__ = ["weeks", "days", "hours", "minutes", "seconds", "start_date", "end_date", "timezone", "jitter"]

  @staticmethod
  def build(sched:dict) -> IntervalTrigger:
    sched.setdefault("weeks"      , 0)    # (int) – number of weeks to wait
    sched.setdefault("days"       , 0)    # (int) – number of days to wait
    sched.setdefault("hours"      , 0)    # (int) – number of hours to wait
    sched.setdefault("minutes"    , 0)    # (int) – number of minutes to wait
    sched.setdefault("seconds"    , 0)    # (int) – number of seconds to wait
    sched.setdefault("start_date" , None) # (datetime|str) – starting point for the interval calculation
    sched.setdefault("end_date"   , None) # (datetime|str) – latest possible date/time to trigger on
    sched.setdefault("timezone"   , None) # (datetime.tzinfo|str) – time zone to use for the date/time calculations
    sched.setdefault("jitter"     , None) # (int|None) – advance or delay the job execution by jitter seconds at most.           
    return IntervalTrigger(**sched)


class CronScheduledBuilder(object):

  __slots__ = ["year", "month", "day", "week", "day_of_week", "hour", "minute", "second", "end_date", "timezone", "jitter"]

  @staticmethod
  def build(sched:Union[dict,str]) -> CronTrigger:
    if isinstance(sched, dict):
      sched.setdefault("year"       , None) # (int|str) - 4-digit year
      sched.setdefault("month"      , None) # (int|str) - month (1-12)
      sched.setdefault("day"        , None) # (int|str) - day of the (1-31)
      sched.setdefault("week"       , None) # (int|str) - ISO week (1-53)
      sched.setdefault("day_of_week", None) # (int|str) - number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
      sched.setdefault("hour"       , None) # (int|str) - hour (0-23)
      sched.setdefault("minute"     , None) # (int|str) - minute (0-59)
      sched.setdefault("second"     , None) # (int|str) - second (0-59)
      sched.setdefault("start_date" , None) # (datetime|str) - earliest possible date/time to trigger on (inclusive)
      sched.setdefault("end_date"   , None) # (datetime|str) - latest possible date/time to trigger on (inclusive)
      sched.setdefault("timezone"   , None) # (datetime.tzinfo|str) - time zone to use for the date/time calculations (defaults to scheduler timezone)
      sched.setdefault("jitter"     , None) # (int|None) – advance or delay the job execution by jitter seconds at most.
      return CronTrigger(**sched)
    else:
      return CronTrigger.from_crontab(sched)

class ScheduledBuilder(object):
  @classmethod
  def getBuilder(cls, scheduled_type="date"):
    builder = DateScheduledBuilder
    if scheduled_type == "interval":
      builder = IntervalScheduledBuilder
    elif scheduled_type == "cron":
      builder = CronScheduledBuilder
    return builder
