import os
import logging
import traceback

# For timezone
from tzlocal import get_localzone

from apscheduler.schedulers.base import (
  STATE_STOPPED, # 0
  STATE_RUNNING, # 1
  STATE_PAUSED   # 2
)
from apscheduler.schedulers.background import BlockingScheduler, BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.base import ConflictingIdError
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# class JobLauncher(ScheduleListener):
class JobLauncher(object):  
  def __init__(self, background=False, deamon=True, **kwargs):
    logging.basicConfig(format="[%(asctime)s] %(message)s", atefmt="%Y-%m-%d %H:%M:%S")
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    if background:
      self.sched = BackgroundScheduler(deamon=deamon) # background
    else:
      self.sched = BlockingScheduler(deamon=deamon) # foreground

    # TODO: Read from configuration file.
    self.sched.configure(
      jobstores={
        # "sqlite": SQLAlchemyJobStore(url='sqlite:///app/database/example.db'),
        # "default": MemoryJobStore()
        "default": SQLAlchemyJobStore(url='sqlite:///app/database/example.db')
      },
      executors={
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
      },
      job_defaults={
        'coalesce': False,
        'max_instances': 3
      },
      timezone=get_localzone() # Asia/Seoul
    )

    self.retried = 0
    self.logger = logging.getLogger('apscheduler')

    super(JobLauncher, self).__init__()

  def start(self):
    try:
      if self.sched.state != STATE_RUNNING:
        self.printJobs(jobstore='default')
        started = self.sched.start()

    except ConflictingIdError as e:
      traceback.print_exc()

    except KeyboardInterrupt as e:
      traceback.print_exc()

    finally:
      pass
      # Remove all remained store.
      # self.sched.remove_all_jobs()
      # for job in self.getJobs():
      #   if job.pending:
      #     job.pause()

      self.logger.info( 'Finished' )
      self.logger.info( self.getJobs() )
      self.printJobs()

  def stop(self, wait=False):
    if self.sched.state == STATE_RUNNING:
      self.sched.shutdown(wait=wait)

  def resume(self):
    if self.sched.state == STATE_RUNNING:
      self.sched.resume()

  def pause(self):
    if self.sched.state == STATE_RUNNING:
      self.sched.pause()

  def addListener(self, listener, types):
    self.sched.add_listener(listener, types)
    
  def addJob(self, job, **kwargs):
    execute, trigger, options = job.build(**kwargs)

    added_job = self.sched.add_job(execute, trigger, **options)

    self.printJobs()

    return added_job

  def getJob(self, job_id):
    return self.sched.get_job(job_id)

  def getJobs(self, jobstore=None):
    return self.sched.get_jobs(jobstore=jobstore)

  def removeJob(self, job_id, jobstore=None):
    return self.sched.remove_job(job_id, jobstore=jobstore)
  
  def removeAllJob(self, jobstore=None):
    return self.sched.remove_all_jobs(jobstore=jobstore)

  def printJobs(self, jobstore=None, out=None):
    return self.sched.print_jobs(jobstore=jobstore, out=None)

  def getJobState(self, job_id=None, jobstore=None):
    state = list()
    
    if job_id is not None:
      job = self.sched.get_job(job_id, jobstore=jobstore)
      
      if job is not None:
        temp = dict()
        temp[job.id] = {
          "next_run_time": job.next_run_time,
          "state": job.pending,
        }
        state.append(temp)

    else:
      for job in self.sched.get_jobs(jobstore=jobstore):
        temp = dict()
        temp[job.id] = {
          "next_run_time": job.next_run_time,
          "state": job.pending,
        }
        state.append(temp)

    return state
