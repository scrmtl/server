from django.db import models

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
    slug = models.SlugField(unique=True)
    def __str__(self):
        return "{0} ({1})".format(self.name, self.description)

class TaskCard (models.Model):
    productBacklog = models.ForeignKey(to='SprintBacklog', on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return "{0} ({1})".format(self.name, self.description)
