from __future__ import unicode_literals

from django.db import models

# Create your models here.


class CompanyInfo(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(null=True)
	homepage = models.TextField(null=True)
