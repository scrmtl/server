"""Serializer for sprints
"""

import logging
from datetime import date, timedelta
from rest_framework import serializers
from django.db.models import QuerySet
import math

from api.models import Sprint, Project, Epic, Feature, Task, Lane

logger = logging.getLogger(__name__)


class SprintStatisticSerializer(serializers.ModelSerializer):
    """Serializer for Task-Cards
    """
    total_duration = serializers.SerializerMethodField()
    remaining_duration = serializers.SerializerMethodField()
    sum_of_done_sp = serializers.SerializerMethodField()
    sum_of_accepted_sp = serializers.SerializerMethodField()
    sum_of_sp = serializers.SerializerMethodField()
    sum_of_tasks = serializers.SerializerMethodField()
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
                  'sum_of_tasks',
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
        if remaining_duration.days > obj.project.sprint_duration:
            return obj.project.sprint_duration
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

    def get_sum_of_tasks(self, obj: Sprint):
        task_queryset: QuerySet = obj.task_cards.all()
        task: Task
        planned_tasks = 0
        for task in task_queryset:
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
        sps = [None] * (obj.project.sprint_duration+1)
        if daily_sp > 0:
            sps = [daily_sp * day for day in
                   reversed(range(0, (obj.project.sprint_duration + 1)))]
        else:
            sps[0] = sum_sp
            sps[obj.project.sprint_duration] = 0
        days = [day for day in range(0, (obj.project.sprint_duration + 1))]

        return {
            'x': days,
            'y': sps
        }

    def get_finished_sp_timeline(self, obj: Sprint):
        task_queryset: QuerySet = obj.task_cards.all()
        days = [int for int in range(0, (obj.project.sprint_duration + 1))]
        day_dates = self.build_day_list(obj)
        daily_sp = [self.get_sum_of_sp(obj)] * \
            (obj.project.sprint_duration + 1)
        daily_sp_count = [0] * (obj.project.sprint_duration+1)
        sum_finished_tasks = 0
        task: Task
        for task in task_queryset:
            if task.done_on in day_dates:
                index = day_dates.index(task.done_on)
                daily_sp_count[index] += task.storypoints

        for i in range(0, (obj.project.sprint_duration + 1)):
            sum_finished_tasks += daily_sp_count[i]
            daily_sp[i] -= sum_finished_tasks

        return {
            'x': days,
            'y': daily_sp
        }

    def get_finished_tasks_timeline(self, obj: Sprint):
        logger.info(f'get finished tasks timeline')
        task_queryset: QuerySet = obj.task_cards.all()
        logger.info(f'--> get tasks: {task_queryset}')
        days = [int for int in range(0, (obj.project.sprint_duration + 1))]
        logger.info(f'--> build day list: {days}')
        day_dates = self.build_day_list(obj)
        logger.info(f'--> List with day_dates: {day_dates}')
        daily_sp = [0] * (obj.project.sprint_duration+1)
        task: Task
        for task in task_queryset:
            logger.info(
                f'   --> test for task: {task} which was done on {task.done_on}')
            if task.done_on in day_dates:
                logger.info(f'      --> Yes task was done in sprint')
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
            obj.start + timedelta(x) for x in range(0, (obj.project.sprint_duration)+1)]
        return day_dates


class ProjectStatisticSerializer(serializers.ModelSerializer):
    """Serializer for Projects
    """
    sum_of_done_sp = serializers.SerializerMethodField()
    sum_of_accepted_sp = serializers.SerializerMethodField()
    sum_of_sp = serializers.SerializerMethodField()
    sum_of_tasks = serializers.SerializerMethodField()
    sum_tasks_rated_not_finished = serializers.SerializerMethodField()
    sum_of_done_tasks = serializers.SerializerMethodField()
    sum_of_accepted_tasks = serializers.SerializerMethodField()
    avg_tasks_in_sprint = serializers.SerializerMethodField()
    avg_sp_in_sprint = serializers.SerializerMethodField()
    worst_sprints_sp = serializers.SerializerMethodField()
    worst_sprints_tasks = serializers.SerializerMethodField()

    avg_finished_tasks_timeline = serializers.SerializerMethodField()
    avg_finished_sp_timeline = serializers.SerializerMethodField()
    finished_sp_timeline = serializers.SerializerMethodField()
    finished_tasks_timeline = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id',
                  'start',
                  'end',
                  'sum_of_done_sp',
                  'sum_of_accepted_sp',
                  'sum_of_sp',
                  'sum_of_tasks',
                  'sum_tasks_rated_not_finished',
                  'sum_of_done_tasks',
                  'sum_of_accepted_tasks',
                  'avg_tasks_in_sprint',
                  'avg_sp_in_sprint',
                  'worst_sprints_sp',
                  'worst_sprints_tasks',
                  'avg_finished_tasks_timeline',
                  'avg_finished_sp_timeline',
                  'finished_sp_timeline',
                  'finished_tasks_timeline')
        read_only_fields = ('start', 'end', 'id')

    def convert_list_to_string(self, org_list, seperator=', '):
        """ Convert list to string, by joining all item in list with given separator.
            Returns the concatenated string """
        return seperator.join(str(v) for v in org_list)

    def get_all_tasks(self, obj: Project):
        # get ids of all lanes
        board_ids = obj.boards.values_list('id', flat=True)
        lane_ids = Lane.objects.filter(
            board__in=board_ids).values_list('id', flat=True)
        tasks = Task.objects.filter(
            lane__in=lane_ids)
        return tasks

    def get_storypoints_by_sprint(self, sprint_ids):
        sprints_with_sp = {}
        for sprint_id in sprint_ids:
            sprint = Sprint.objects.get(id=sprint_id)
            storypoints = 0
            for task in sprint.task_cards.all():
                if (task.status == Task.Status.ACCEPTED):
                    storypoints += task.storypoints
            sprints_with_sp[sprint.number] = storypoints
        sorted_sprints_with_sp = dict(
            sorted(sprints_with_sp.items(), key=lambda item: item[0]))
        return sorted_sprints_with_sp

    def get_tasks_by_sprint(self, sprint_ids):
        sprints_with_sp = {}
        for sprint_id in sprint_ids:
            sprint = Sprint.objects.get(id=sprint_id)
            accepted_tasks = 0
            for task in sprint.task_cards.all():
                if (task.status == Task.Status.ACCEPTED):
                    accepted_tasks += 1
            sprints_with_sp[sprint.number] = accepted_tasks
        sorted_sprints_with_sp = dict(
            sorted(sprints_with_sp.items(), key=lambda item: item[0]))
        return sorted_sprints_with_sp

    def get_accepted_sprint_ids(self, obj: Project):
        sprint_ids = obj.sprints.filter(
            status=Sprint.SprintStatus.ACCEPTED).values_list('id', flat=True)
        return sprint_ids

    def get_sum_of_task_sp(self, tasks: QuerySet):
        sum_of_sp = 0
        for task in tasks.all():
            sum_of_sp += task.storypoints
        return sum_of_sp

    def get_sum_of_done_sp(self, obj: Project):
        task_queryset: QuerySet = self.get_all_tasks(obj).all()
        task: Task
        done_sp = 0
        for task in task_queryset:
            if task.status == Task.Status.DONE:
                done_sp += task.storypoints
        return done_sp

    def get_sum_of_accepted_sp(self, obj: Project):
        task_queryset: QuerySet = self.get_all_tasks(obj).all()
        task: Task
        accepted_sp = 0
        for task in task_queryset:
            if task.status == Task.Status.ACCEPTED:
                accepted_sp += task.storypoints
        return accepted_sp

    def get_sum_of_sp(self, obj: Project):
        task_queryset: QuerySet = self.get_all_tasks(obj).all()
        task: Task
        sp = 0
        for task in task_queryset:
            sp += task.storypoints
        return sp

    def get_sum_of_tasks(self, obj: Project):
        task_queryset: QuerySet = self.get_all_tasks(obj).all()
        task: Task
        planned_tasks = 0
        for task in task_queryset:
            planned_tasks += 1
        return planned_tasks

    def get_sum_of_done_tasks(self, obj: Project):
        task_queryset: QuerySet = self.get_all_tasks(obj).all()
        task: Task
        done_tasks = 0
        for task in task_queryset:
            if task.status == Task.Status.DONE:
                done_tasks += 1
        return done_tasks

    def get_sum_of_accepted_tasks(self, obj: Project):
        task_queryset: QuerySet = self.get_all_tasks(obj).all()
        task: Task
        accepted_tasks = 0
        for task in task_queryset:
            if task.status == Task.Status.ACCEPTED:
                accepted_tasks += 1
        return accepted_tasks

    def get_sum_tasks_rated_not_finished(self, obj: Project):
        task_queryset: QuerySet = self.get_all_tasks(obj).all()
        task: Task
        rated_tasks = 0
        for task in task_queryset:
            if (task.status != Task.Status.ACCEPTED and
                    task.status != Task.Status.DONE and
                    task.storypoints == 0):

                rated_tasks += 1
        return rated_tasks

    def get_avg_tasks_in_sprint(self, obj: Project):
        # get tasks of accepted sprints
        sprint_ids = self.get_accepted_sprint_ids(obj)
        task_queryset = Task.objects.filter(
            sprint__in=sprint_ids)
        task: Task
        accepted_tasks = 0
        if (len(sprint_ids) < 1):
            return 0
        for task in task_queryset:
            if (task.status == Task.Status.ACCEPTED):
                accepted_tasks += 1
        return round(accepted_tasks / len(sprint_ids), 2)

    def get_avg_sp_in_sprint(self, obj: Project):
        # get tasks of accepted sprints
        sprint_ids = self.get_accepted_sprint_ids(obj)
        task_queryset = Task.objects.filter(
            sprint__in=sprint_ids)
        task: Task
        storypoints = 0
        if (len(sprint_ids) < 1):
            return 0
        for task in task_queryset:
            if (task.status == Task.Status.ACCEPTED):
                storypoints += task.storypoints
        return round(storypoints / len(sprint_ids), 2)

    def get_worst_sprints_sp(self, obj: Project):
        accepted_sprint_ids = self.get_accepted_sprint_ids(obj)
        sprints = self.get_storypoints_by_sprint(accepted_sprint_ids)
        sprints = dict(
            sorted(sprints.items(), key=lambda item: item[1]))
        worst_sprints = self.convert_list_to_string(
            list(sprints.keys())[:3])
        return worst_sprints

    def get_worst_sprints_tasks(self, obj: Project):
        accepted_sprint_ids = self.get_accepted_sprint_ids(obj)
        sprints = self.get_tasks_by_sprint(accepted_sprint_ids)
        sprints = dict(
            sorted(sprints.items(), key=lambda item: item[1]))
        worst_sprints = self.convert_list_to_string(
            list(sprints.keys())[:3])
        return worst_sprints

    def get_avg_finished_tasks_timeline(self, obj: Project):
        logger.info(f'get avg finished tasks')
        number_sprints = len(self.get_accepted_sprint_ids(obj))
        avg_tasks = self.get_avg_tasks_in_sprint(obj)
        tasks = [avg_tasks] * number_sprints
        sprints = list(range(1, number_sprints+1))
        return{
            'x': sprints,
            'y': tasks
        }

    def get_avg_finished_sp_timeline(self, obj: Project):

        number_sprints = len(self.get_accepted_sprint_ids(obj))
        avg_storypoints = self.get_avg_sp_in_sprint(obj)
        storypoints = [avg_storypoints] * number_sprints
        sprints = list(range(1, number_sprints+1))
        return{
            'x': sprints,
            'y': storypoints
        }

    def get_finished_sp_timeline(self, obj: Project):
        accepted_sprint_ids = self.get_accepted_sprint_ids(obj)
        sprints = self.get_storypoints_by_sprint(accepted_sprint_ids)

        return {
            'x': sprints.keys(),
            'y': sprints.values()
        }

    def get_finished_tasks_timeline(self, obj: Project):
        accepted_sprint_ids = self.get_accepted_sprint_ids(obj)
        sprints = self.get_tasks_by_sprint(accepted_sprint_ids)

        return {
            'x': sprints.keys(),
            'y': sprints.values()
        }

    def build_day_list(self, obj: Project):
        """
        This function return a list with days of the project
        """
        day_dates = [
            obj.start + timedelta(int) for int in range(1, (obj.sprint_duration + 1))]
        return day_dates
