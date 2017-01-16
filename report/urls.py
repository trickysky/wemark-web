#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/11/10


from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^s/scan_count/(?P<bid>\d+)$', views.scan_count),
    url(r'^s/code_count/(?P<bid>\d+)$', views.code_count),
    url(r'^s/award_amount', views.award_amount),
    url(r'^s/accepted_and_award_amount/(?P<bid>\d+)$', views.accepted_and_award_amount),
    url(r'^s/batch_id', views.batch_id),
    url(r'^s/daily_count/(?P<bid>\d+)$', views.daily_count),
    url(r'^s/accepted_rate', views.accepted_rate),
]
