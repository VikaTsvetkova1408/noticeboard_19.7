import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from . import jobs as core_jobs

scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


def start():
    if settings.DEBUG:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler.add_job(core_jobs.delete_old_job_executions,
                      'cron',
                      id='delete_old_job_executions',
                      day_of_week='wed',
                      hour='00',
                      minute='00',
                      replace_existing=True)

    scheduler.start()
