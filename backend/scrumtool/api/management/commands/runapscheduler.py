# runapscheduler.py
import logging
from datetime import date
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from api.models.sprint import Sprint
from api.models.card import Task
from api.models import Lane
from api.models.board import Board

logger = logging.getLogger(__name__)


def my_job():
    #  Your job processing logic here...
    set_sprint_in_progress_handler(
        Sprint.objects.filter(start=date.today()))
    set_sprint_done_handler(Sprint.objects.filter(end=date.today()))
    set_sprint_accepted_handler(Sprint.objects.filter(end=date.today()))
    move_cards_handler(
        Sprint.objects.filter(start=date.today()))


def set_sprint_in_progress_handler(sprints_today):
    sprint: Sprint
    for sprint in sprints_today:
        if sprint.status == Sprint.SprintStatus.PLANNED:
            sprint.status = Sprint.SprintStatus.IN_PROGRESS
            sprint.save()


def set_sprint_done_handler(sprints_today):
    sprint: Sprint
    for sprint in sprints_today:
        if sprint.status == Sprint.SprintStatus.IN_PROGRESS:
            sprint.status = Sprint.SprintStatus.DONE
            sprint.save()


def set_sprint_accepted_handler(sprints_today):
    sprint: Sprint
    for sprint in sprints_today:
        if sprint.status == Sprint.SprintStatus.DONE:
            sprint.status = Sprint.SprintStatus.ACCEPTED
            sprint.save()


def move_cards_handler(sprints_today):
    sprint: Sprint
    for sprint in sprints_today:

        if sprint.status == Sprint.SprintStatus.IN_PROGRESS:
            # get lane of PB
            pb_board: Board = sprint.project.boards.get(
                board_type=Board.BoardType.PB)
            sb_board: Board = sprint.project.boards.get(
                board_type=Board.BoardType.SB)
            growing_lane: Lane = pb_board.lanes.get(name__icontains='Growning')
            next_lane: Lane = sb_board.lanes.get(name__icontains='Next')
            # get tasks of PB
            tasks = Task.objects.filter(lane=growing_lane.id)
            task: Task
            for task in tasks.all():
                task.lane = next_lane
                task.save()


def midnight_job():
    #  Your job processing logic here...
    pass


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            midnight_job,
            trigger=CronTrigger(day="*", hour="0"),  # Every 10 seconds
            id="midnight_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'midnight_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="10", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
