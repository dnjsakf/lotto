import pprint
import apscheduler.events as events

__all__ = [
  "ScheduleListener"
]

class ScheduleListener(object):
  def __init__(self):
    self.addListener(self.schedule_listener, events.EVENT_SCHEDULER_START | events.EVENT_SCHEDULER_SHUTDOWN)
    self.addListener(self.jobs_listener, events.EVENT_JOB_EXECUTED | events.EVENT_JOB_ERROR | events.EVENT_JOB_MISSED)

  def jobs_listener(self, event):
    print( 'EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED:', event )
    pprint.pprint({
      "job_id": event.job_id,
      "jobstore": event.jobstore,
      "retval": event.retval,
      "scheduled_run_time": event.scheduled_run_time,
      "alias": event.alias,
      "exception": event.exception,
      "traceback": event.traceback
    })

  def schedule_listener(self, event):
    ''' [ alias, code ] '''
    print( 'EVENT_SCHEDULER_START:', event )
    pprint.pprint({
      "code": event.code,
      "alias": event.alias
    })