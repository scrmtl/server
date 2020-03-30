from rest_framework import serializers
from scrumtoolHome.models import Steplist
from . import step_serializer


class StepListSerializer(serializers.ModelSerializer):
    """Serializer for a steplist

    """
    checklistitem_set = step_serializer.StepSerializer(many=True)

    class Meta:
        model = Steplist
        fields = ('name', 'checklistitem_set')
        depth = 1


class StepListSerializerCommon(serializers.ModelSerializer):
    """Serializer for a steplist

    """

    class Meta:
        model = Steplist
        fields = ('name',)
