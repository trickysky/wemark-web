from __future__ import unicode_literals

from django.db import models

# Create your models here.


class CompanyInfo(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(null=True)
	homepage = models.TextField(null=True)
	urlprefix = models.CharField(max_length=255, null=True)


class AwardSetting(models.Model):
	total_prize = models.BigIntegerField(null=True)
	rate = models.IntegerField(null=True)
	max_prize = models.IntegerField(null=True)
	min_prize = models.IntegerField(null=True)
