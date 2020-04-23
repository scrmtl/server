from django.contrib import admin

from . import models
# Register your models here.

admin.site.register(models.Task)
admin.site.register(models.SteplistItem)
admin.site.register(models.Steplist)
admin.site.register(models.Project)
admin.site.register(models.Lane)
admin.site.register(models.Label)
admin.site.register(models.Feature)
admin.site.register(models.Epic)
admin.site.register(models.Board)
admin.site.register(models.File)
