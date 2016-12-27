#!/usr/bin/python
# -*- coding=UTF-8 -*-
from django.shortcuts import render
import requests
from django.http import JsonResponse


# Create your views here.

def set_index():
	base_data = {}
	base_data['app_name'] = u'生产赋码'
	base_data['page_name'] = u'百威啤酒'
	base_data['page_desc'] = u''
	base_data['barcode_options'] = [
		{'text': 'barcode_option1', 'value': 'barcode_value_1'},
		{'text': 'barcode_option2', 'value': 'barcode_value_2'},
		{'text': 'barcode_option3', 'value': 'barcode_value_3'}
	]

	base_data['factory_options'] = []
	factories = requests.get("http://api.wemarklinks.net:81/factory").json()
	if factories and factories['code'] == 0:
		for factory in factories['data']:
			base_data['factory_options'].append({'text': factory['factoryName'], 'value': factory['id']})

	return base_data


def index(request):
	return render(request, 'managesite/index.html', set_index())


def batch(request):
	if request.method == 'POST':
		return JsonResponse({'method': 'POST'})
	else:
		return JsonResponse({'method': 'GET'})
