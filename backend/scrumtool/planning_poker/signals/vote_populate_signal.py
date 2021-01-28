from api.models import PlatformUser
from planning_poker.models import Vote, PokerVote, PokerVoting
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=Vote)
def update_poker_vote_status(sender, instance: Vote, created, update_fields, **kwargs):
    poker_vote: PokerVote = instance.poker_vote
    poker_voting: PokerVoting = poker_vote.poker_voting
    if (poker_vote.votes.count() > 0 and
            poker_vote.status == PokerVote.PokerStatus.NOTSTARTED):
        poker_vote.status = PokerVote.PokerStatus.WAITING
        poker_vote.save()
    if (poker_voting.voters.count() == poker_vote.votes.count() and
            poker_vote.status == PokerVote.PokerStatus.WAITING):
        poker_vote.status = PokerVote.PokerStatus.FINISHED
        poker_vote.save()
