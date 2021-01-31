from django.contrib import admin

from planning_poker import models

admin.site.register(models.PokerVoting)
admin.site.register(models.PokerVote)
admin.site.register(models.Vote)
