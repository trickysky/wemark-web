from __future__ import unicode_literals

from django.db import models

# Create your models here.


class CompanyInfo(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(null=True)
	homepage = models.TextField(null=True)
	urlprefix = models.CharField(max_length=255)


class AwardSetting(models.Model):
	total_prize = models.BigIntegerField(max_length=8)
	rate = models.IntegerField(max_length=2)
	max_prize = models.IntegerField(max_length=4)
	min_prize = models.IntegerField(max_length=4)
