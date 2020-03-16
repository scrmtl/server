""" admin definitions for the app -
such definitions are needed to access model class instances
from the Django admin site.
"""
from django.contrib import admin
from .models import ProductBacklog, SprintBacklog, TaskCard, Checklist, ChecklistItem


admin.site.register(ProductBacklog)
admin.site.register(SprintBacklog)
admin.site.register(TaskCard)
admin.site.register(Checklist)
admin.site.register(ChecklistItem)
