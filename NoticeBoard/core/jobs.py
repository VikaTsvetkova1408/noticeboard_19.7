from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util


@util.close_old_connections
def delete_old_job_executions(max_age=604800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
