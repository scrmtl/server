"""Receiver to add an default steplist to task after creation
    """
from api.models import Steplist, Task
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Task)
def create_task_defaults(sender, instance: Task, created, **kwargs):
    if created:
        Steplist.objects.create(task=instance, name='DefaultSteplist')
