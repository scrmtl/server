from rest_framework import serializers
from scrumtoolHome.models import ChecklistItem


class StepSerializer(serializers.ModelSerializer):
    """Serializer for a step

    """
    class Meta:
        model = ChecklistItem
        fields = ('id', 'text', 'checked', 'numbering')
