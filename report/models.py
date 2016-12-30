from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Source(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255)
	description = models.TextField()
	created_time = models.DateTimeField()
	update_time = models.DateTimeField()


class Operation(models.Model):
	id = models.AutoField(primary_key=True)
	select = models.BooleanField()
	delete = models.BooleanField()
	update = models.BooleanField()
	insert = models.BooleanField()