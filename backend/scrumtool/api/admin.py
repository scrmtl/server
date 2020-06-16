from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from . import models
# Register your models here.

from .forms import ScrumUserCreationForm, ScrumUserChangeForm
from .models import ScrumUser


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


class ScrumUserAdmin(UserAdmin):
    add_form = ScrumUserCreationForm
    form = ScrumUserChangeForm
    model = ScrumUser
    list_display = ['email', 'username', 'name']


admin.site.register(ScrumUser, ScrumUserAdmin)
