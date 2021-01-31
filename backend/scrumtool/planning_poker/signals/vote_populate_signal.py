from api.models import PlatformUser, ProjectUser, ProjectRole, Task
from planning_poker.models import Vote, PokerVote, PokerVoting
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import logging

stdlogger = logging.getLogger(__name__)
available_storypoints = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55]


@receiver(post_save, sender=Vote)
def update_poker_vote_status(sender, instance: Vote, created, update_fields, **kwargs):
    poker_vote: PokerVote = instance.poker_vote
    poker_voting: PokerVoting = poker_vote.poker_voting

    # get number of scrum master by filtering ProjectUser

    number_of_scrum_master = ProjectUser.objects.filter(
        project=poker_voting.project,
        plattform_user__in=poker_voting.voters.all(),
        role=ProjectRole.objects.get(id=ProjectRole.SM)
    ).count()
    if (poker_vote.votes.count() > 0 and
            poker_vote.status == PokerVote.PokerStatus.NOTSTARTED):
        poker_vote.status = PokerVote.PokerStatus.WAITING
        poker_vote.save()

    stdlogger.info(f'voters in poker voting: {poker_voting.voters.count()} ' +
                   f'voters in poker vote: {poker_vote.votes.count()} ' +
                   f'scrum master in project: {number_of_scrum_master}')
    if (poker_voting.voters.count() ==
        poker_vote.votes.count() + number_of_scrum_master and
            poker_vote.status == PokerVote.PokerStatus.WAITING):
        poker_vote.status = PokerVote.PokerStatus.FINISHED
        poker_vote.save()


@receiver(post_save, sender=PokerVote)
def update_task_storypoints(sender, instance: PokerVote, created, update_fields, **kwargs):
    if instance.status == PokerVote.PokerStatus.ACCEPTED:
        instance.task.storypoints = get_end_storypoints(instance)
        instance.task.save()


def get_avg_storypoints(obj: PokerVote):
    # get tasks of accepted sprints
    storypoints = 0
    skipped = 0
    for vote in obj.votes.all():
        storypoints += vote.storypoints
        if vote.storypoints == 0:
            skipped += 1
    if (obj.votes.count() - skipped) <= 0:
        return 0
    return storypoints / (obj.votes.count() - skipped)


def get_end_storypoints(obj: PokerVote):
    sp = round(get_avg_storypoints(obj))
    return min(available_storypoints, key=lambda x: abs(x-sp))
