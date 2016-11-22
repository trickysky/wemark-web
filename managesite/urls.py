#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/11/22

from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index),
]