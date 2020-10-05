'''
Manger for project to add extra methods
'''
from django.db import models


class TemplateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_template=True)
