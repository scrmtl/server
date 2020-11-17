from datetime import date
from django.contrib.auth.models import Group
from api.models.card import Task, Epic, Feature
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Task)
def set_done_on_task(sender, instance: Task, update_fields, **kwargs):
    if instance.status == Task.Status.DONE:
        instance.done_on = date.today()
    else:
        instance.done_on = None


@receiver(pre_save, sender=Epic)
def set_done_on_epic(sender, instance: Epic, update_fields, **kwargs):
    if instance.status == Epic.Status.DONE:
        instance.done_on = date.today()
    else:
        instance.done_on = None


@receiver(pre_save, sender=Feature)
def set_done_on_feature(sender, instance: Feature, update_fields, **kwargs):
    if instance.status == Feature.Status.DONE:
        instance.done_on = date.today()
    else:
        instance.done_on = None
