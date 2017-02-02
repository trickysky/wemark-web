#!/usr/bin/python
# -*- coding=UTF-8 -*-
# trickysky
# 2016/11/22
from django.shortcuts import render
from wemark.commons.services import FactoryService, CompanyService, ProductService, AwardSettingService
from oauth2.commons.security import Subject


# Create your views here.
def set_index(request):
	company_info = CompanyService.get_company()
	award_setting = AwardSettingService.get_award_setting()
	base_data = {
		'app_name': u'信息录入',
		'page_name': u'信息录入',
		'page_desc': u'',
		'factory_list': [],
		'product_list': [],
		'company_name': company_info.get('name') if company_info else None,
		'company_description': company_info.get('description') if company_info else None,
		'company_homepage': company_info.get('homepage') if company_info else None,
		'award_total_prize': award_setting.get('total_prize') if award_setting else 0,
		'award_rate': award_setting.get('award_rate') if award_setting else 0,
		'award_min_prize': award_setting.get('min_prize') if award_setting else 0,
		'award_max_prize': award_setting.get('max_prize') if award_setting else 0
	}
	subject = Subject.get_instance(request.session)
	products = ProductService.get_product_list()
	if products and products.get('code') == 0:
		for product in products.get('data'):
			if subject.has_role('root') or product.get('createdBy') == subject.get_user_info(request).get('id'):
				base_data['product_list'].append({
					'product_id': product['id'],
					'product_name': product['name'],
					'product_unit': product['unit'],
					'product_barcode': product['barcode'],
					'product_intro': product['intro'],
					'product_icon': product['icon'],
					'product_status': product['status'],
					'product_images': product['images'],
					'product_description': product['description'],
				})
	factories = FactoryService.get_factory_list()
	if factories and factories.get('code') == 0:
		for factory in factories['data']:
			if subject.has_role('root') or factory.get('createdBy') == subject.get_user_info(request).get('id'):
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
	return render(request, 'edit_info/index.html', set_index(request))
