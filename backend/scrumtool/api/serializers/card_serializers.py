"""Serializers for Cards
"""
from rest_framework import serializers
from ..models import Card, Task, Feature, Epic, Label, File


class LabelSerializer(serializers.ModelSerializer):
    """Serializer for all Labels
    """

    class Meta:
        model = Label
        fields = ('title', 'color', 'id')


class FileSerializer(serializers.ModelSerializer):
    """Serializer for all Files
    """
    size = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    filetype = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'photo', 'size', 'name', 'filetype')

    def get_size(self, obj):
        file_size = ''
        if obj.photo and hasattr(obj.photo, 'size'):
            file_size = obj.photo.size
        return file_size

    def get_name(self, obj):
        file_name = ''
        if obj.photo and hasattr(obj.photo, 'name'):
            file_name = obj.photo.name
        return file_name

    def get_filetype(self, obj):
        filename = obj.photo.name
        return filename.split('.')[-1]


class CardSerializer(serializers.ModelSerializer):
    """Base-class serializer for cards.
    Other cards will inherits from this class
    """

    class Meta:
        model = Card
        abstract = True
        fields = ('id', 'name',
                  'description', 'numbering',
                  'storypoints', 'status'
                  )


class EpicSerializer(serializers.ModelSerializer):
    """Serializer for Epic-Cards
    """
    labels = LabelSerializer(many=True, required=False)
    files = FileSerializer(many=True, required=False)

    class Meta:
        model = Epic
        fields = CardSerializer.Meta.fields + ('labels', 'files')


class FeatureSerializer(serializers.ModelSerializer):
    """Serializer for Feature-Cards
    """
    labels = LabelSerializer(many=True, required=False)
    files = FileSerializer(many=True, required=False)

    class Meta:
        model = Feature
        fields = CardSerializer.Meta.fields + ('labels', 'files')


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task-Cards
    """
    labels = LabelSerializer(many=True, required=False)
    files = FileSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = CardSerializer.Meta.fields + ('labels', 'files')
