#!/usr/bin/python
# -*- coding=UTF-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
import time

from wemark.commons.services import FactoryService, BatchService, CompanyService
from oauth2.commons.security import Subject


# Create your views here.

def set_index(request):
    base_data = {}
    base_data['app_name'] = u'生产赋码'
    base_data['page_name'] = CompanyService.get_company().get('name')
    base_data['page_desc'] = u'批次管理'
    base_data['barcode_options'] = [
        {'text': 'barcode_option1', 'value': 'barcode_value_1'},
        {'text': 'barcode_option2', 'value': 'barcode_value_2'},
        {'text': 'barcode_option3', 'value': 'barcode_value_3'}
    ]
    base_data['factory_options'] = []
    factories = FactoryService.get_factory_list()
    if factories and factories['code'] == 0:
        for factory in factories['data']:
            base_data['factory_options'].append({'text': factory['factoryName'], 'value': factory['id']})

    base_data['batch_list'] = set_batch_list(request, BatchService.get_batch_list())
    return base_data


def index(request):
    return render(request, 'managesite/index.html', set_index(request))


def new_batch(request):
    subject = Subject.get_instance(request.session)
    user = subject.get_user_info()

    body = request.POST
    return BatchService.create_batch(
        factory_id=body.get('factory_id'),
        incode_factory=body.get('incode_factory'),
        outcode_factory=body.get('outcode_factory'),
        casecode_factory=body.get('casecode_factory'),
        case_count=body.get('case_count'),
        case_size=body.get('case_size'),
        unit_count=body.get('unit_count'),
        barcode=body.get('barcode'),
        expired_time=body.get('expired_time'),
        product_info=body.get('product_info'),
        callback_uri=body.get('callback_uri'),
        created_by=user['id'],
        updated_by=user['id']
    )


def get_factory_by_id(factory_id):
    if not factory_id:
        return None
    response = FactoryService.get_factory(factory_id=factory_id)
    if response['code'] == 0:
        return response['data'].get('factoryName')
    else:
        return None


def set_batch_list(request, response):
    subject = Subject.get_instance(request.session)
    batch_list = []
    for b in response['data']:
        if b.get('createdBy') == subject.get_user_info(request).get('id'):
            batch_list.append({
                'expired_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(b['updatedTime'] / 1000)),
                'barcode': b['barcode'],
                'unit_count': b['unitCount'],
                'inner_code_factory': get_factory_by_id(b['incodeFactory'] if b['incodeFactory'] else None),
                'outer_code_factory': get_factory_by_id(b['outcodeFactory'] if b['outcodeFactory'] else None),
                'case_code_factory': get_factory_by_id(b['casecodeFactory'] if b['casecodeFactory'] else None),
                'factory_id': get_factory_by_id(b['factoryId'] if b['factoryId'] else None),
                'prod_info': b['productInfo'] if b['productInfo'] else None,
                'batch_id': b['id'],
                'status': b['status']
            })
    return batch_list


def batch(request):
    if request.method == 'POST':
        new_batch_response = new_batch(request)
        response = {'code': new_batch_response['code'],
                    'msg': 'new batch success' if new_batch_response['code'] == 0 else 'new batch error'}
        return JsonResponse(response)
    elif request.method == 'GET':
        response = BatchService.get_batch_list()
        return JsonResponse(response)
