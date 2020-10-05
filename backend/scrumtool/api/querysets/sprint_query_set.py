'''
Querysets for project to add extra methods
'''

from django.db import models
from datetime import date, timedelta, datetime


class SprintQuerySet(models.QuerySet):
    def sprints_starting_today(self):
        self.filter(start=datetime.date(datetime.now()))

    def sprints_ending_today(self):
        self.filter(end=datetime.date(datetime.now()))
