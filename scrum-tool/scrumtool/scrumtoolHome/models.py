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
    def __str__(self):
        return "{0} ({1})".format(self.name, self.description)


class adminUser (models.Model):
    firstName = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=100)

class normalUser (models.Model):
    firstName = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=100)
