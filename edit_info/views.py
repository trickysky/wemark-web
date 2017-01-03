#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/11/22
import requests
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.



def set_index():
	base_data = {
		'app_name': u'信息录入',
		'page_name': u'信息录入',
		'page_desc': u''
	}
	return base_data


def index(request):
	return render(request, 'edit_info/index.html', set_index())
