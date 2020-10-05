from django.contrib.auth.models import Group
from api.models.users import PlatformUser
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=PlatformUser)
def create_user_profile(sender, instance: PlatformUser, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='standard'))
