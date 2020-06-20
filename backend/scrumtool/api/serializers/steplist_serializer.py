"""Serializers for Steplists
"""
from rest_framework import serializers
from ..models import Steplist, SteplistItem, Task
from . import step_serializer
import logging
logger = logging.getLogger(__name__)


class StepListSerializer(serializers.ModelSerializer):
    """Serializer for a steplist

    """
    steplistitem_set = step_serializer.StepSerializer(many=True)
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), required=True)

    class Meta:
        model = Steplist
        fields = ('name', 'steplistitem_set', 'id', 'task')
        depth = 1

    def create(self, validated_data):
        steplistitem_set_data = validated_data.pop('steplistitem_set')

        instance = super().create(validated_data)
        instance.save()

        instance = self.update_steplistitem(instance, steplistitem_set_data)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        steplistitem_set_data = validated_data.pop('steplistitem_set')

        instance = super().update(instance, validated_data)
        instance.save()

        instance = self.update_steplistitem(instance, steplistitem_set_data)
        instance.save()

        return instance

    def update_steplistitem(self, instance, steplistitem_set_data):
        steplistitem_instance = None
        for steplistitem in steplistitem_set_data:
            if (('id' in steplistitem) and SteplistItem.objects.filter(
                    id=steplistitem['id']).exists()):
                steplistitem_instance = SteplistItem.objects.get(
                    id=steplistitem['id'])
            steplistitem['steplist'] = instance.id
            steplistitem_serializer = step_serializer.StepSerializer(
                data=steplistitem, instance=steplistitem_instance)
            if steplistitem_serializer.is_valid():
                steplistitem_instance = steplistitem_serializer.save()
                logger.info('Save new steplistitem: %s with id: %s',
                            steplistitem_serializer.validated_data,
                            steplistitem_instance.id)
                instance.steplistitem_set.add(steplistitem_instance)
                steplistitem_instance = None
        return instance


class StepListSerializerForCards(serializers.ModelSerializer):
    """Serializer for a steplist

    """
    steplistitem_set = step_serializer.StepSerializer(
        many=True, required=False)
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), required=False)

    class Meta:
        model = Steplist
        fields = ('name', 'steplistitem_set', 'id', 'task')
        depth = 1
        # to override readonly
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
            },
        }

    def create(self, validated_data):
        steplistitem_set_data = validated_data.pop('steplistitem_set')

        instance = super().create(validated_data)
        instance.save()

        instance = self.update_steplistitem(instance, steplistitem_set_data)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        steplistitem_set_data = validated_data.pop('steplistitem_set')

        instance = super().update(instance, validated_data)
        instance.save()

        instance = self.update_steplistitem(instance, steplistitem_set_data)
        instance.save()
        instance = self.delete_not_send_steplistitem(
            instance, steplistitem_set_data)
        instance.save()

        return instance

    def update_steplistitem(self, instance, steplistitem_set_data):
        steplistitem_instance = None
        for steplistitem in steplistitem_set_data:
            if (('id' in steplistitem) and SteplistItem.objects.filter(
                    id=steplistitem['id']).exists()):
                steplistitem_instance = SteplistItem.objects.get(
                    id=steplistitem['id'])
            steplistitem['steplist'] = instance.id
            steplistitem_serializer = step_serializer.StepSerializer(
                data=steplistitem, instance=steplistitem_instance)
            if steplistitem_serializer.is_valid():
                steplistitem_instance = steplistitem_serializer.save()
                logger.info('Save new steplistitem: %s with id: %s',
                            steplistitem_serializer.validated_data,
                            steplistitem_instance.id)
                instance.steplistitem_set.add(steplistitem_instance)
                steplistitem_instance = None
        return instance

    def delete_not_send_steplistitem(self, instance, steplistitem_set_data):
        id_list = list()
        for steplistitem in steplistitem_set_data:
            if (('id' in steplistitem) and SteplistItem.objects.filter(
                    id=steplistitem['id']).exists()):
                id_list.append(steplistitem['id'])
            else:
                continue
        for steplistitem in instance.steplistitem_set.all():
            if steplistitem.id not in id_list:
                steplistitem.delete()
        return instance


class StepListSerializerCommon(serializers.ModelSerializer):
    """Serializer for a steplist

    """
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), required=False)

    class Meta:
        model = Steplist
        fields = ('name', 'id', 'task')
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }
