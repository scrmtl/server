from huey import crontab
from huey.contrib.djhuey import db_periodic_task, periodic_task
from api.models import Sprint
from django.db.models.query import QuerySet


@periodic_task(crontab(minute='*/1'))
def SprintDateReached():
    qs_starting: QuerySet = Sprint.timed.sprints_starting_today
    qs_ending: QuerySet = Sprint.timed.sprints_ending_today
    _sprint: Sprint
    for _sprint in qs_starting:
        if _sprint.status == Sprint.SprintStatus.IN_PLANNING:
            _sprint.status = Sprint.SprintStatus.IN_PROGRESS
            _sprint.save()

    for _sprint in qs_ending:
        if _sprint.status == Sprint.SprintStatus.IN_PROGRESS:
            _sprint.status = Sprint.SprintStatus.DONE
            _sprint.save()


@periodic_task(crontab(minute='*/1'))
def every_other_minute():
    print('This task runs every 2 minutes.', 35)
