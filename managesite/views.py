#!/usr/bin/python
# -*- coding=UTF-8 -*-
from django.shortcuts import render

# Create your views here.

def set_index():
	base_data = {}
	base_data['app_name'] = u'管理终端'
	base_data['page_name'] = u'管理终端'
	base_data['page_desc'] = u'管理终端页面'
	return base_data

def index(request):
	return render(request, 'managesite/index.html', set_index())