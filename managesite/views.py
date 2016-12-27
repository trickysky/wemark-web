#!/usr/bin/python
# -*- coding=UTF-8 -*-
from django.shortcuts import render
import requests
from django.http import JsonResponse
import requests

# Create your views here.

server_url = 'http://api.wemarklinks.net:81'


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


def new_batch(request):
	body = request.POST
	params = {}
	params['factory_id'] = body.get('factory_id')
	params['incode_factory'] = body.get('incode_factory')
	params['outcode_factory'] = body.get('outcode_factory')
	params['casecode_factory'] = body.get('casecode_factory')
	params['case_count'] = body.get('case_count')
	params['case_size'] = body.get('case_size')
	params['unit_count'] = body.get('unit_count')
	params['barcode'] = body.get('barcode')
	params['expired_time'] = body.get('expired_time')
	params['product_info'] = body.get('product_info')
	params['callback_uri'] = body.get('callback_uri')
	response = requests.post('%s/batch' % server_url, data=params).json()
	return response


def get_batch():
	return requests.get('%s/batch' % server_url).json()


def batch(request):
	if request.method == 'POST':
		new_batch_response = new_batch(request)
		response = {'code': new_batch_response['code'],
		            'msg': 'new batch success' if new_batch_response['code'] == 0 else 'new batch error'}
		return JsonResponse(response)
	elif request.method == 'GET':
		response = get_batch()
		return JsonResponse(response)
