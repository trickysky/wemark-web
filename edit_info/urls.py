#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/12/31

from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index),
]