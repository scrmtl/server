from datetime import date
from django.contrib.auth.models import Group
from api.models.card import Task, Epic, Feature
from django.db.models.signals import pre_save
from django.dispatch import receiver

import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Task)
def set_done_on_task(sender, instance: Task, update_fields, **kwargs):
    logger.info(f'---------------task signal----------------')
    if not Task.objects.filter(id=instance.id).exists():
        return
    old_instance = Task.objects.get(id=instance.id)
    logger.info(f'new status of task {instance} is {instance.status}')
    logger.info(f'old status of task {old_instance} is {old_instance.status}')
    if (instance.status == Task.Status.DONE and
            old_instance.status != Task.Status.DONE):
        logger.info(f'overwrite task date_on with {date.today()}')
        instance.done_on = date.today()
    elif instance.status == Task.Status.ACCEPTED:
        return
    else:
        instance.done_on = None


@receiver(pre_save, sender=Epic)
def set_done_on_epic(sender, instance: Epic, update_fields, **kwargs):
    if not Epic.objects.filter(id=instance.id).exists():
        return
    old_instance = Epic.objects.get(id=instance.id)
    if (instance.status == Epic.Status.DONE and
            old_instance.status != Epic.Status.DONE):
        instance.done_on = date.today()
    elif instance.status == Epic.Status.ACCEPTED:
        return
    else:
        instance.done_on = None


@receiver(pre_save, sender=Feature)
def set_done_on_feature(sender, instance: Feature, update_fields, **kwargs):
    if not Feature.objects.filter(id=instance.id).exists():
        return
    old_instance = Feature.objects.get(id=instance.id)
    if (instance.status == Feature.Status.DONE and
            old_instance.status != Feature.Status.DONE):
        instance.done_on = date.today()
    elif instance.status == Feature.Status.ACCEPTED:
        return
    else:
        instance.done_on = None
