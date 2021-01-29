# runapscheduler.py
import logging
import os
from datetime import date, timedelta
from django.conf import settings

from asgiref.sync import sync_to_async

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from api.models.sprint import Sprint
from api.models.card import Task
from api.models import Lane
from api.models.board import Board

from planning_poker.models import PokerVoting, PokerVote

LOGLEVEL = os.getenv('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)

'''
def my_job():
    logger.info("---------------------Executing my_job-----------------------")
    logger.info(
        f"Sprints today: {Sprint.objects.filter(start=date.today()).all()}")
    task = Task.objects.get(id=1)
    task.name = 'nananananana Batman'
    task.save()
'''


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
                f"--> Project boards: {sprint.project.boards}")
            pb_board: Board = sprint.project.boards.get(
                board_type=Board.BoardType.PB)
            logger.info(
                f"   --> PB : {pb_board}")
            sb_board: Board = sprint.project.boards.get(
                board_type=Board.BoardType.SP)
            logger.info(
                f"   --> SB : {sb_board}")
            growing_lane: Lane = pb_board.lanes.get(name__icontains='Growning')
            ready_lane: Lane = pb_board.lanes.get(name__icontains='Ready')
            next_lane: Lane = sb_board.lanes.get(name__icontains='Next')
            logger.info(
                f"Move cards from lane {growing_lane}\
                     located in board {pb_board} to lane\
                     {next_lane} located in board {sb_board}")
            # get tasks of PB
            tasks = Task.objects.filter(
                lane__in=[growing_lane.id, ready_lane.id], sprint=sprint.id)
            task: Task
            for task in tasks.all():
                if task.sprint is not None:
                    logger.info(
                        f"Moved card {task} \n")
                    task.lane = next_lane
                    task.status = Task.Status.NOT_STARTED
                    task.save()


def move_cards_to_archive_handler(sprints_today):
    sprint: Sprint
    for sprint in sprints_today:
        logger.info(
            f"--> Sprint: {sprint} ends today")
        if (sprint.status == Sprint.SprintStatus.DONE or
                sprint.status == Sprint.SprintStatus.ACCEPTED):
            # get lane of SB
            logger.info(
                f"--> Sprint today: {sprint.project.boards}")
            ab_board: Board = sprint.project.boards.get(
                board_type=Board.BoardType.AB)
            logger.info(
                f"   --> AB : {ab_board}")
            sb_board: Board = sprint.project.boards.get(
                board_type=Board.BoardType.SP)
            logger.info(
                f"   --> SB : {sb_board}")
            done_lane: Lane = sb_board.lanes.get(name__icontains='Done')

            archive_lane: Lane = create_or_get_lane(ab_board, sprint)
            logger.info(
                f"   --> Move cards from lane {done_lane} " +
                f"located in board {sb_board} to lane " +
                f"{archive_lane} located in board {ab_board}")
            # get tasks of Sprint Backlog
            tasks = Task.objects.filter(
                lane=done_lane.id,
                sprint=sprint.id,
                status=Task.Status.ACCEPTED)
            task: Task
            for task in tasks.all():
                if task.sprint is not None:
                    logger.info(
                        f"      -->Moved card {task} \n")
                    task.lane = archive_lane
                    task.save()


def create_or_get_lane(ab_board: Board, sprint: Sprint):
    if ab_board.lanes.filter(
            name__icontains=sprint.create_lane_name()).exists():
        return ab_board.lanes.get(
            name__icontains=sprint.create_lane_name())
    else:
        # create Name
        lane_name = sprint.create_lane_name()

        # Add new Lane with Sprint Infos to Board
        sprint_lane = Lane(
            board=ab_board,
            name=lane_name,
        )
        sprint_lane.save()
        return sprint_lane


def set_poker_vote_status(end_poker_voting):
    poker_voting: PokerVoting
    poker_vote: PokerVote
    for poker_voting in end_poker_voting:
        for poker_vote in poker_voting.poker_votes.all():
            poker_vote.status = PokerVote.PokerStatus.FINISHED
            poker_vote.save()
            logger.info(f"-->Finished PokerVote: {poker_vote}")


def hourly_job():
    # This job actually starts at 10 o'clock because the server aka
    # the old laptop is only online from 8:00-22:00
    logger.info(
        "---------------------Executing hourly_job-----------------------")
    start_sprints = Sprint.objects.filter(
        start__lte=date.today(),
        end__gte=date.today()).all()
    end_sprints = Sprint.objects.filter(
        end__range=(date.today() -
                    timedelta(days=30), date.today())).all()
    logger.info(
        f"Sprints starting: {start_sprints}")
    logger.info(
        f"Sprints ending: {end_sprints}")
    logger.info(f"--> set_sprint_in_progress_handler (Sprint Start)")
    set_sprint_in_progress_handler(start_sprints)
    logger.info(f"--> set_sprint_done_handler (Sprint End)")
    set_sprint_done_handler(end_sprints)
    logger.info(f"--> set_sprint_accepted_handler (Sprint End)")
    set_sprint_accepted_handler(end_sprints)
    logger.info(f"--> move_cards_handler (Sprint Start)")
    move_cards_handler(start_sprints)
    logger.info(f"--> move_cards_to_archive_handler (Sprint End)")
    move_cards_to_archive_handler(end_sprints)

    # Run schedular for Planning poker

    end_poker_voting = PokerVoting.objects.filter(
        end__gte=date.today()
    ).all()
    logger.info(f"Finishing pokerVotings: {end_poker_voting}")
    set_poker_vote_status(end_poker_voting)


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        '''
        scheduler.add_job(
            my_job,
            trigger =CronTrigger(second ="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
        '''
        scheduler.add_job(
            hourly_job,
            # Every 10 seconds
            trigger=CronTrigger(day="*", hour="*", minute="10"),
            id="hourly_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'hourly_job'.")

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
