from rest_framework import serializers
from .. import models


class ScrumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ScrumUser
        fields = ('email', 'username', )
