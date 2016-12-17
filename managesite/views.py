#!/usr/bin/python
# -*- coding=UTF-8 -*-
from django.shortcuts import render

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
	base_data['factory_options'] = [
		{'text': 'factory_option1', 'value': 'factory_value_1'},
		{'text': 'factory_option2', 'value': 'factory_value_2'},
		{'text': 'factory_option3', 'value': 'factory_value_3'}
	]
	base_data['inner_code_factory_options'] = ['inner_code_factory_option1', 'inner_code_factory_option2', 'inner_code_factory_option3']
	base_data['outer_code_factory_options'] = ['outer_code_factory_option1', 'outer_code_factory_option2', 'outer_code_factory_option3']
	base_data['box_code_factory_options'] = ['box_code_factory_option1', 'box_code_factory_option2', 'box_code_factory_option3']
	return base_data

def index(request):
	return render(request, 'managesite/index.html', set_index())