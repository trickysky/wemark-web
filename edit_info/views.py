#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/11/22
import requests
from django.http import JsonResponse
from django.shortcuts import render
from wemark_config import LOCAL_PORT, LOCAL_HOST

# Create your views here.



def set_index():
	base_data = {
		'app_name': u'信息录入',
		'page_name': u'信息录入',
		'page_desc': u'',
		'factory_list': []
	}
	factories = requests.get('http://%s:%s/s/factory' % (LOCAL_HOST, LOCAL_PORT)).json()
	if factories and factories['code'] == 0:
		for factory in factories['data']:
			base_data['factory_list'].append({
				'factory_id': factory['id'],
				'factory_name': factory['factoryName'],
				'factory_type': factory['type'],
				'factory_ip': factory['location'],
				'factory_region': factory['region'],
				'factory_status': factory['status'],
				'factory_owner': factory['owner'],
				'factory_owner_phone': factory['ownerMobile'],
				'factory_owner_email': factory['ownerEmail'],
			})
	return base_data


def index(request):
	return render(request, 'edit_info/index.html', set_index())
