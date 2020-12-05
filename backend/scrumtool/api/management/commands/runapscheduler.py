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
    logger.info("---------------------Executing my_job-----------------------")
    logger.info(
        f"Sprints today: {Sprint.objects.filter(start=date.today()).all()}")
    set_sprint_in_progress_handler(
        Sprint.objects.filter(start=date.today()).all())
    set_sprint_done_handler(Sprint.objects.filter(end=date.today()).all())
    set_sprint_accepted_handler(Sprint.objects.filter(end=date.today()).all())
    move_cards_handler(
        Sprint.objects.filter(start=date.today()).all())


def set_sprint_in_progress_handler(sprints_today):
    sprint: Sprint
    for sprint in sprints_today:

        if (sprint.status == Sprint.SprintStatus.PLANNED) and \
                (len(sprint.task_cards.all()) > 0):
            logger.info(
                f"Set status {Sprint.SprintStatus.IN_PROGRESS}\
                     in Sprint {sprint}")
            sprint.status = Sprint.SprintStatus.IN_PROGRESS
            sprint.save()


def set_sprint_done_handler(sprints_today):
    sprint: Sprint
    for sprint in sprints_today:
        if sprint.status == Sprint.SprintStatus.IN_PROGRESS:
            logger.info(
                f"Set status {Sprint.SprintStatus.DONE}\
                     in Sprint {sprint}")
            sprint.status = Sprint.SprintStatus.DONE
            sprint.save()


def set_sprint_accepted_handler(sprints_today):
    sprint: Sprint
    task: Task
    all_tasks_accepted = True
    for sprint in sprints_today:
        for task in sprint.task_cards.all():
            if task.status != Task.Status.ACCEPTED:
                all_tasks_accepted = False
        if sprint.status == Sprint.SprintStatus.DONE and all_tasks_accepted:

            logger.info(
                f"Set status {Sprint.SprintStatus.ACCEPTED}\
                     in Sprint {sprint}")
            sprint.status = Sprint.SprintStatus.ACCEPTED
            sprint.save()


def move_cards_handler(sprints_today):
    sprint: Sprint
    for sprint in sprints_today:
        logger.info(
            f"--> Sprint today: {sprint}")
        if sprint.status == Sprint.SprintStatus.IN_PROGRESS:
            # get lane of PB
            logger.info(
                f"--> Sprint today: {sprint.project.boards}")
            pb_board: Board = sprint.project.boards.get(
                board_type=Board.BoardType.PB)
            logger.info(
                f"   --> PB : {pb_board}")
            sb_board: Board = sprint.project.boards.get(
                board_type=Board.BoardType.SP)
            logger.info(
                f"   --> SB : {sb_board}")
            growing_lane: Lane = pb_board.lanes.get(name__icontains='Growning')
            next_lane: Lane = sb_board.lanes.get(name__icontains='Next')
            logger.info(
                f"Move cards from lane {growing_lane}\
                     located in board {pb_board} to lane\
                     {next_lane} located in board {sb_board}")
            # get tasks of PB
            tasks = Task.objects.filter(lane=growing_lane.id)
            task: Task
            for task in tasks.all():
                if task.sprint is not None:
                    logger.info(
                        f"Moved card {task}")
                    task.lane = next_lane
                    task.save()


def midnight_job():
    # This job actually starts at 10 o'clock because the server aka
    # the old laptop is only online from 8:00-22:00
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
            trigger=CronTrigger(second="*/59"),  # Every 10 seconds
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
