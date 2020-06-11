from rest_framework import serializers
from .. import models
from django.utils.translation import gettext_lazy as _


class ScrumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ScrumUser
        fields = ('email', 'username', )
