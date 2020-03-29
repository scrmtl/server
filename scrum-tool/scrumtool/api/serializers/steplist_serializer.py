from rest_framework import serializers
from scrumtoolHome.models import Checklist
from . import step_serializer


class StepListSerializer(serializers.ModelSerializer):
    """Serializer for a steplist

    """
    checklistitem_set = step_serializer.StepSerializer(many=True)

    class Meta:
        model = Checklist
        fields = ('name', 'checklistitem_set')
        depth = 1
