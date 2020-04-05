"""Serializers for Cards
"""
from rest_framework import serializers
from ..models import Card, Task, Feature, Epic, Label


class LabelSerializer(serializers.ModelSerializer):
    """Serializer for all Labels
    """

    class Meta:
        model = Label
        fields = ('title', 'color', 'id')


class CardSerializer(serializers.ModelSerializer):
    """Base-class serializer for cards.
    Other cards will inherits from this class
    """

    class Meta:
        model = Card
        abstract = True
        fields = ('id', 'name',
                  'description', 'numbering',
                  'storypoints', 'status',
                  )


class EpicSerializer(serializers.ModelSerializer):
    """Serializer for Epic-Cards
    """
    labels = LabelSerializer(many=True)

    class Meta:
        model = Epic
        fields = CardSerializer.Meta.fields + ('labels',)


class FeatureSerializer(serializers.ModelSerializer):
    """Serializer for Feature-Cards
    """
    labels = LabelSerializer(many=True)

    class Meta:
        model = Feature
        fields = CardSerializer.Meta.fields + ('labels',)


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task-Cards
    """
    labels = LabelSerializer(many=True)

    class Meta:
        model = Task
        fields = CardSerializer.Meta.fields + ('labels',)
