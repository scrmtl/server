""" This file contains database definitions
"""
from django.db import models


class ProductBacklog(models.Model):
    """The ProductBacklog stores different SprintBacklogs

    """
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.slug)


class SprintBacklog(models.Model):
    """The SprintBacklog stores all Information for a sprint
    """
    productBacklog = models.ForeignKey(
        to='ProductBacklog', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    # slug = models.SlugField(unique=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.description)


class TaskCard(models.Model):
    """A TaskCard contains all information concerning a task.
    Including the Checklist
    """
    sprintBacklog = models.ForeignKey(
        to='SprintBacklog', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    storypoints = models.IntegerField(default=0)
    label_frontend = models.BooleanField(default=False)
    label_backend = models.BooleanField(default=False)
    label_other = models.BooleanField(default=False)

    def __str__(self):
        return "{0} ({1}) {2} {3} {4} {5} {5}".format(
            self.name,
            self.description,
            self.storypoints,
            self.label_backend,
            self.label_frontend,
            self.label_other)


class Checklist(models.Model):
    """ A Checklist contains all elements of a checklist
    """
    taskCard = models.ForeignKey(to='TaskCard', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)

    def __str__(self):
        return "{0} ".format(self.name)


class ChecklistItem(models.Model):
    """ A ChecklistItem describes a Task that has to be done
    """
    checklist = models.ForeignKey(to='Checklist', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    checked = models.BooleanField()

    def __str__(self):
        return "{0}({1}): {2} ".format(self.name, self.checklist, self.checked)
