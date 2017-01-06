#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/11/10


from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^s/scan_code', views.scan_code),
    url(r'^s/award_amount', views.award_amount),
    url(r'^s/award_count', views.award_count),
]
