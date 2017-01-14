#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2017/1/3


from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^factory$', views.factory),
    url(r'^factory/(?P<factory_id>\d+)$', views.factory_by_id),
    url(r'^batch$', views.batch),
    url(r'^company$', views.company),
    url(r'^product$', views.product),
    url(r'^product/(?P<product_id>\d+)$', views.product_by_id),
]
