'''
Querysets for project to add extra methods
'''

from django.db import models
from api.models import Project


class ProjectQuerySet(models.QuerySet):
    def sprints_starting_today():
        pass

    def sprints_ending_today():
        pass
