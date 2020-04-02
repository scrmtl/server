"""Serializers for steps
"""
from rest_framework import serializers
from scrumtoolHome.models import SteplistItem


class StepSerializer(serializers.ModelSerializer):
    """Serializer for a step

    """
    class Meta:
        model = SteplistItem
        fields = ('id', 'text', 'checked', 'numbering')
