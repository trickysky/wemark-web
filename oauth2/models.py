from __future__ import unicode_literals

from django.db import models


# Create your models here.

class ModelWithDateTime(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TargetResource(ModelWithDateTime):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()


class Operation(ModelWithDateTime):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()


class Permission(ModelWithDateTime):
    id = models.AutoField(primary_key=True)
    resource = models.ForeignKey(TargetResource)
    operation = models.ForeignKey(Operation)


class UserRole(ModelWithDateTime):
    id = models.AutoField(primary_key=True)
    permissions = models.ManyToManyField(Permission)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
