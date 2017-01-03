#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2017/1/3


from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^factory', views.factory),
	url(r'^batch', views.batch),
]