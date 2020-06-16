"""Serializers for steps
"""
from rest_framework import serializers
from ..models import SteplistItem, Steplist


class StepSerializer(serializers.ModelSerializer):
    """Serializer for a step

    """
    steplist = serializers.PrimaryKeyRelatedField(
        queryset=Steplist.objects.all(), required=False)

    class Meta:
        model = SteplistItem
        fields = ('id', 'text', 'checked', 'numbering', 'steplist')
        # to override readonly
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }
