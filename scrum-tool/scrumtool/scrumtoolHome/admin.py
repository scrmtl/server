""" admin definitions for the app -
such definitions are needed to access model class instances
from the Django admin site.
"""
from django.contrib import admin
from . import models


admin.site.register(models.ProductBacklog)
admin.site.register(models.SprintBacklog)
admin.site.register(models.TaskCard)
admin.site.register(models.Checklist)
admin.site.register(models.ChecklistItem)
