"""Serializers for Cards
"""
import logging
from rest_framework import serializers
from api.models import Card, Task, Feature, Epic, Label, File, \
    Steplist, PlatformUser, Lane
from .steplist_serializer import StepListSerializerForCards, \
    StepListSerializerCommon
from .simple_history_serializers import HistoricalRecordField
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
    lane = serializers.PrimaryKeyRelatedField(
        queryset=Lane.objects.all(), required=False)

    class Meta:
        model = Card
        abstract = True
        fields = ('id', 'name',
                  'description', 'numbering',
                  'storypoints', 'status',
                  'lane', 'sprint'
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
        instance.lane = validated_data.get('lane', instance.lane)
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


class TaskSerializerFull(serializers.ModelSerializer):
    """Serializer for Task-Cards
    """
    labels = LabelSerializer(many=True, required=False)
    # files = FileSerializer(many=True, required=False)
    steplists = StepListSerializerForCards(many=True, required=False)
    feature = serializers.PrimaryKeyRelatedField(
        queryset=Feature.objects.all(), required=True)
    assigned_users = serializers.PrimaryKeyRelatedField(
        queryset=PlatformUser.objects.all(), required=False, many=True)
    number_of_steps = serializers.SerializerMethodField()
    number_of_open_steps = serializers.SerializerMethodField()
    history = HistoricalRecordField(read_only=True)

    class Meta:
        model = Task
        fields = CardSerializer.Meta.fields + \
            ('feature', 'assigned_users', 'labels', 'steplists',
             'number_of_steps', 'number_of_open_steps',
             'history',)

    def get_number_of_steps(self, obj):
        steps = 0
        for steplist in obj.steplists.all():
            steps += steplist.steplistitem_set.count()
        return steps

    def get_number_of_open_steps(self, obj):
        open_steps = 0
        for steplist in obj.steplists.all():
            for step in steplist.steplistitem_set.all():
                if not step.checked:
                    open_steps += 1
        return open_steps

    def create(self, validated_data):
        labels_data = None
        steplists_data = None
        if 'labels' in validated_data:
            labels_data = validated_data.pop('labels')
        if 'steplists' in validated_data:
            steplists_data = validated_data.pop('steplists')

        instance = super().create(validated_data)
        instance.save()

        if labels_data is not None:
            instance = self.update_label(instance, labels_data)
            instance.save()
            instance = self.create_non_existing_label(instance, labels_data)
            instance.save()
        if steplists_data is not None:
            instance = self.update_steplist(instance, steplists_data)
            instance.save()

        return instance

    def update(self, instance, validated_data):
        labels_data = None
        steplists_data = None
        if 'labels' in validated_data:
            labels_data = validated_data.pop('labels')
        if 'steplists' in validated_data:
            steplists_data = validated_data.pop('steplists')

        instance = super().update(instance, validated_data)
        instance.save()

        if labels_data is not None:
            instance = self.update_label(instance, labels_data)
            instance.save()
            instance = self.create_non_existing_label(instance, labels_data)
            instance.save()
            instance = self.delete_not_send_labels(instance, labels_data)
            instance.save()
        if steplists_data is not None:
            instance = self.update_steplist(instance, steplists_data)
            instance.save()
            instance = self.delete_not_send_steplists(instance, steplists_data)
            instance.save()
        return instance

    def update_label(self, instance, labels_data):
        '''
        Updates existing labels. Not existing labels are skipped.
        '''
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
            else:
                continue
            # TODO Benutzer über fehlende Argumente informieren
            label_serializer = LabelSerializer(
                data=label, instance=label_instance)
            if label_serializer.is_valid():
                label_instance = label_serializer.save()
                logger.info('Update existing label: %s with id: %s',
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
            for step in steplist['steplistitem_set']:
                step['steplist'] = steplist['id']
            steplist_serializer = StepListSerializerForCards(
                data=steplist, instance=steplist_instance)
            steplist_serializer.is_valid()
            logger.info(steplist_serializer.errors)
            if steplist_serializer.is_valid():
                steplist_instance = steplist_serializer.save()
                logger.info('Save new steplist: %s with id: %s',
                            steplist_serializer.validated_data,
                            steplist_instance.id)
                steplist_instance.save()
                steplist_instance = None

        return instance

    def delete_not_send_steplists(self, instance, steplists_data):
        id_list = list()
        for steplist in steplists_data:
            if (('id' in steplist) and Steplist.objects.filter(
                    id=steplist['id']).exists()):
                id_list.append(steplist['id'])
            else:
                continue
        for steplist in instance.steplists.all():
            if steplist.id not in id_list:
                steplist.delete()
        return instance

    def create_non_existing_label(self, instance, labels_data):
        '''
        Create new label if label does not exists
        '''
        label_instance = None
        for label in labels_data:
            if ((
                ('id' in label) and not
                Label.objects.filter(
                    id=label['id']).exists())
                or
                (('title' in label) and not
                 Label.objects.filter(
                    title=label['title']).exists())):
                label_serializer = LabelSerializer(
                    data=label)
            else:
                continue
            if label_serializer.is_valid():
                label_instance = label_serializer.save()
                logger.info('Create new label: %s with id: %s',
                            label_serializer.validated_data, label_instance.id)
                instance.labels.add(label_instance)
                label_instance = None
        return instance

    def delete_not_send_labels(self, instance, labels_data):
        '''
        delete existing label from task
        '''
        id_list = list()
        for label in labels_data:
            if (('id' in label) and Label.objects.filter(
                    id=label['id']).exists()):
                id_list.append(label['id'])
            else:
                continue
        for label in instance.labels.all():
            if label.id not in id_list:
                instance.labels.remove(label)
        return instance


class ChangeSerializer(serializers.Serializer):
    diff_changes = serializers.SerializerMethodField()
    history_user = serializers.PrimaryKeyRelatedField(
        queryset=Task.history.model.objects.all(), required=False)
    history_date = serializers.DateTimeField()

    def get_diff_changes(self, obj):
        if not obj.prev_record:
            return
        delta = obj.diff_against(obj.prev_record)
        change_obj = []
        for change in delta.changes:
            changes = {}
            changes["field"] = change.field
            changes["old"] = change.old
            changes["new"] = change.new
            change_obj.append(changes)
        return change_obj


class ChangesListSerializer(serializers.ListSerializer):
    child = ChangeSerializer()


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task-Cards
    """
    labels = LabelSerializer(
        many=True,
        required=False,
        read_only=False)
    # serializers.PrimaryKeyRelatedField(
    #    many=True,
    #    required=False,
    #    queryset=Label.objects.all())
    # files = FileSerializer(many=True, required=False)
    steplists = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        read_only=False,
        queryset=Steplist.objects.all())
    feature = serializers.PrimaryKeyRelatedField(
        queryset=Feature.objects.all(),
        required=True)
    assigned_users = serializers.PrimaryKeyRelatedField(
        queryset=PlatformUser.objects.all(), required=False, many=True)
    number_of_steps = serializers.SerializerMethodField()
    number_of_open_steps = serializers.SerializerMethodField()
    history = ChangesListSerializer(required=False,
                                    read_only=True)

    class Meta:
        model = Task
        fields = CardSerializer.Meta.fields + \
            ('feature', 'assigned_users', 'labels', 'steplists',
             'number_of_steps', 'number_of_open_steps', 'history',)

    def get_number_of_steps(self, obj):
        steps = 0
        for steplist in obj.steplists.all():
            steps += steplist.steplistitem_set.count()
        return steps

    def get_number_of_open_steps(self, obj):
        open_steps = 0
        for steplist in obj.steplists.all():
            for step in steplist.steplistitem_set.all():
                if not step.checked:
                    open_steps += 1
        return open_steps
