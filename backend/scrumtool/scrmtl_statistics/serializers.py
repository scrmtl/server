"""Serializer for sprints
"""
from datetime import date, timedelta
from rest_framework import serializers
from django.db.models import QuerySet
import math

from api.models import Sprint, Project, Epic, Feature, Task


class SprintStatisticSerializer(serializers.ModelSerializer):
    """Serializer for Task-Cards
    """
    total_duration = serializers.SerializerMethodField()
    remaining_duration = serializers.SerializerMethodField()
    sum_of_done_sp = serializers.SerializerMethodField()
    sum_of_accepted_sp = serializers.SerializerMethodField()
    sum_of_sp = serializers.SerializerMethodField()
    sum_of_planned_tasks = serializers.SerializerMethodField()
    sum_of_done_tasks = serializers.SerializerMethodField()
    sum_of_accepted_tasks = serializers.SerializerMethodField()

    planned_sp_timeline = serializers.SerializerMethodField()
    finished_sp_timeline = serializers.SerializerMethodField()
    finished_tasks_timeline = serializers.SerializerMethodField()

    class Meta:
        model = Sprint
        fields = ('id',
                  'start',
                  'end',
                  'status',
                  'total_duration',
                  'remaining_duration',
                  'sum_of_done_sp',
                  'sum_of_accepted_sp',
                  'sum_of_sp',
                  'sum_of_planned_tasks',
                  'sum_of_done_tasks',
                  'sum_of_accepted_tasks',
                  'planned_sp_timeline',
                  'finished_sp_timeline',
                  'finished_tasks_timeline')
        read_only_fields = ('start', 'end', 'number')

    def get_total_duration(self, obj: Sprint):
        if obj.project is None:
            return 0
        return obj.project.sprint_duration

    def get_remaining_duration(self, obj: Sprint):
        remaining_duration = 0
        start = date.today()
        end = obj.end
        if (end is None) or (end < start):
            return 0
        remaining_duration = end - start
        return remaining_duration.days

    def get_sum_of_done_sp(self, obj: Sprint):
        task_queryset: QuerySet = obj.task_cards.all()
        task: Task
        done_sp = 0
        for task in task_queryset:
            if task.status == Task.Status.DONE:
                done_sp += task.storypoints
        return done_sp

    def get_sum_of_accepted_sp(self, obj: Sprint):
        task_queryset: QuerySet = obj.task_cards.all()
        task: Task
        accepted_sp = 0
        for task in task_queryset:
            if task.status == Task.Status.ACCEPTED:
                accepted_sp += task.storypoints
        return accepted_sp

    def get_sum_of_sp(self, obj: Sprint):
        task_queryset: QuerySet = obj.task_cards.all()
        task: Task
        sp = 0
        for task in task_queryset:
            sp += task.storypoints
        return sp

    def get_sum_of_planned_tasks(self, obj: Sprint):
        task_queryset: QuerySet = obj.task_cards.all()
        task: Task
        planned_tasks = 0
        for task in task_queryset:
            if task.status == Task.Status.PLANNED:
                planned_tasks += 1
        return planned_tasks

    def get_sum_of_done_tasks(self, obj: Sprint):
        task_queryset: QuerySet = obj.task_cards.all()
        task: Task
        done_tasks = 0
        for task in task_queryset:
            if task.status == Task.Status.DONE:
                done_tasks += 1
        return done_tasks

    def get_sum_of_accepted_tasks(self, obj: Sprint):
        task_queryset: QuerySet = obj.task_cards.all()
        task: Task
        accepted_tasks = 0
        for task in task_queryset:
            if task.status == Task.Status.ACCEPTED:
                accepted_tasks += 1
        return accepted_tasks

    def get_planned_sp_timeline(self, obj: Sprint):
        task_queryset: QuerySet = obj.task_cards.all()
        # get number of days
        sum_sp = self.get_sum_of_sp(obj)
        daily_sp = math.floor((sum_sp / obj.project.sprint_duration))
        sps = [daily_sp *
               int for int in reversed(range(1, (obj.project.sprint_duration + 1)))]
        days = [int for int in range(1, (obj.project.sprint_duration + 1))]

        return {
            'x': days,
            'y': sps
        }

    def get_finished_sp_timeline(self, obj: Sprint):
        task_queryset: QuerySet = obj.task_cards.all()
        days = [int for int in range(1, (obj.project.sprint_duration + 1))]
        day_dates = self.build_day_list(obj)
        daily_sp = [self.get_sum_of_sp(obj)] * obj.project.sprint_duration
        daily_sp_count = [0] * obj.project.sprint_duration
        sum_finished_tasks = 0
        task: Task
        for task in task_queryset:
            if task.done_on in day_dates:
                index = day_dates.index(task.done_on)
                daily_sp_count[index] += task.storypoints

        for i in range(0, (obj.project.sprint_duration)):
            sum_finished_tasks += daily_sp_count[i]
            daily_sp[i] -= sum_finished_tasks

        return {
            'x': days,
            'y': daily_sp
        }

    def get_finished_tasks_timeline(self, obj: Sprint):
        task_queryset: QuerySet = obj.task_cards.all()
        days = [int for int in range(1, (obj.project.sprint_duration + 1))]
        day_dates = self.build_day_list(obj)
        daily_sp = [0] * obj.project.sprint_duration
        task: Task
        for task in task_queryset:
            if task.done_on in day_dates:
                index = day_dates.index(task.done_on)
                daily_sp[index] += 1
        return {
            'x': days,
            'y': daily_sp
        }

    def build_day_list(self, obj: Sprint):
        """
        This function return a list with days of the sprint
        """
        day_dates = [
            obj.start + timedelta(int) for int in range(1, (obj.project.sprint_duration + 1))]
        return day_dates
