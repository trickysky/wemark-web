#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/11/22

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^s/batch$', views.batch),
    url(r'^s/batch/(?P<batch_id>\d+)$', views.batch_by_id),
    url(r'^s/batch/send_code$', views.batch_send_code),
    url(r'^s/batch/enable_code$', views.batch_enable_code),
]
