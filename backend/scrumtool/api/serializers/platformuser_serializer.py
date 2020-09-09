from rest_framework import serializers
from .. import models
from django.utils.translation import gettext_lazy as _


class PlattformUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlatformUser
        fields = ('id',
                  'email',
                  'username',
                  'name',)
