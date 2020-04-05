"""Serializers for Cards
"""
from rest_framework import serializers
from ..models import Card, Task, Feature, Epic, Label


class LabelSerializer(serializers.ModelSerializer):
    """Serializer for all Labels
    """

    class Meta:
        model = Label
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    """Base-class serializer for cards.
    Other cards will inherits from this class
    """
    label = LabelSerializer(many=True)

    class Meta:
        model = Card
        abstract = True
        fields = ('id', 'name',
                  'description', 'numbering',
                  'storypoints', 'status',
                  'label')


class EpicSerializer(serializers.ModelSerializer):
    """Serializer for Epic-Cards
    """

    class Meta:
        model = Epic
        fields = CardSerializer.Meta.fields


class FeatureSerializer(serializers.ModelSerializer):
    """Serializer for Feature-Cards
    """

    class Meta:
        model = Feature
        fields = CardSerializer.Meta.fields


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task-Cards
    """

    class Meta:
        model = Task
        fields = CardSerializer.Meta.fields
