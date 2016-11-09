#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/11/9


from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.login, name='login'),
]