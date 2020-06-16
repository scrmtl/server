"""Serializers for Cards
"""
from rest_framework import serializers
from ..models import Card, Task, Feature, Epic, Label, File, Steplist
from .steplist_serializer import StepListSerializerForCards
import logging
logger = logging.getLogger(__name__)


class LabelSerializer(serializers.ModelSerializer):
    """Serializer for all Labels
    """

    class Meta:
        model = Label
        fields = ('title', 'color', 'id')
        # to override readonly
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }


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
                  'storypoints', 'status',
                  )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.numbering = validated_data.get(
            'numbering', instance.numbering)
        instance.storypoints = validated_data.get(
            'storypoints', instance.storypoints)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class EpicSerializer(serializers.ModelSerializer):
    """Serializer for Epic-Cards
    """
    labels = LabelSerializer(many=True, required=False)
    # files = FileSerializer(many=True, required=False)
    steplists = StepListSerializerForCards(many=True, required=False)

    class Meta:
        model = Epic
        fields = CardSerializer.Meta.fields + ('labels', 'steplists')


class FeatureSerializer(serializers.ModelSerializer):
    """Serializer for Feature-Cards
    """
    labels = LabelSerializer(many=True, required=False)
    # files = FileSerializer(many=True, required=False)
    steplists = StepListSerializerForCards(many=True, required=False)

    class Meta:
        model = Feature
        fields = CardSerializer.Meta.fields + ('labels', 'steplists')


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task-Cards
    """
    labels = LabelSerializer(many=True, required=False)
    # files = FileSerializer(many=True, required=False)
    steplists = StepListSerializerForCards(many=True, required=False)
    feature = serializers.PrimaryKeyRelatedField(
        queryset=Feature.objects.all(), required=True)

    class Meta:
        model = Task
        fields = CardSerializer.Meta.fields + \
            ('labels', 'steplists', 'feature')

    def update(self, instance, validated_data):
        labels_data = validated_data.pop('labels')
        steplists_data = validated_data.pop('steplists')

        instance = super().update(instance, validated_data)
        instance.save()

        instance = self.update_label(instance, labels_data)
        instance.save()

        instance = self.update_steplist(instance, steplists_data)
        instance.save()

        return instance

    def update_label(self, instance, labels_data):
        label_instance = None

        for label in labels_data:
            if (('id' in label) and Label.objects.filter(
                    id=label['id']).exists()):
                label_instance = Label.objects.get(
                    id=label['id'])

            elif(('title' in label) and
                 Label.objects.filter(
                    title=label['title']).exists()):
                label_instance = Label.objects.get(
                    title=label['title'])
            # TODO Benutzer über fehlende Argumente informieren
            label_serializer = LabelSerializer(
                data=label, instance=label_instance)
            if label_serializer.is_valid():
                label_instance = label_serializer.save()
                logger.info('Save new label: %s with id: %s',
                            label_serializer.validated_data, label_instance.id)
                instance.labels.add(label_instance)
                label_instance = None
        return instance

    def update_steplist(self, instance, steplists_data):
        steplist_instance = None
        for steplist in steplists_data:
            if (('id' in steplist) and Steplist.objects.filter(
                    id=steplist['id']).exists()):
                steplist_instance = Steplist.objects.get(
                    id=steplist['id'])
            steplist['task'] = instance.id
            steplist_serializer = StepListSerializer(
                data=steplist, instance=steplist_instance)

            if steplist_serializer.is_valid():
                steplist_instance = steplist_serializer.save()
                logger.info('Save new steplist: %s with id: %s',
                            steplist_serializer.validated_data,
                            steplist_instance.id)
                steplist_instance.save()
                steplist_instance = None

        return instance
