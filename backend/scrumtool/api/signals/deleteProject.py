"""Receiver to add an default steplist to task after creation
    """
from api.models import Project, ProjectUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver

import logging
logger = logging.getLogger(__name__)


@receiver(pre_delete, sender=Project)
def create_task_defaults(sender, instance: Project, *args, **kwargs):
    for project_user in instance.project_users.all():
        logger.info("Deleted %s", project_user)
        project_user.delete()
