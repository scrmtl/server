"""Receiver to add an default steplist to task after creation
    """
from api.models import Sprint, Lane, Board
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Sprint)
def create_sprint_lane_in_backlog(sender, instance: Sprint, created, **kwargs):
    if (not created) and (instance.status == Sprint.SprintStatus.DONE):
        # Get Archive Board
        archive_board: Board = instance.project.boards.get(
            board_type=Board.BoardType.AB)
        # create Name
        lane_name = instance.create_lane_name()
        # if lane exists skip
        if archive_board.lanes.filter(
                name__icontains=instance.create_lane_name()).exists():
            return

        # Add new Lane with Sprint Infos to Board
        sprint_lane = Lane(
            board=archive_board,
            name=lane_name,
            numbering=instance.number
        )
        sprint_lane.save()
