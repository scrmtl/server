from django.db import models
from django.contrib.auth.models import User


class ProductBacklog (models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return "{0} ({1})".format(self.name, self.slug)

class SprintBacklog (models.Model):
    productBacklog = models.ForeignKey(to='ProductBacklog', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    #slug = models.SlugField(unique=True)
    def __str__(self):
        return "{0} ({1})".format(self.name, self.description)

class TaskCard (models.Model):
    sprintBacklog = models.ForeignKey(to='SprintBacklog', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    storypoints = models.IntegerField(default=0)
    label_frontend = models.BooleanField(default=False)
    label_backend = models.BooleanField(default=False)
    label_other = models.BooleanField(default=False)

    def __str__(self):
        return "{0} ({1}) {2} {3} {4} {5} {5}".format(self.name, self.description, self.storypoints, self.label_backend, self.label_frontend, self.label_other)
