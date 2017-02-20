#!/usr/bin/python
# -*- coding=UTF-8 -*-
from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import time
import StringIO
import wemark.commons.utils as utils
from wemark.commons.constants import *
from wemark.commons.services import FactoryService, BatchService, CompanyService, ProductService
from wemark.commons.response import ResponseEntity
from oauth2.commons.security import Subject


# Create your views here.

def __get_batch_code(batch_id, assign_type, section_id):
    cache_expires_in = 60
    cache_key = __generate_key('%s_%d_%d' % (batch_id, assign_type, section_id))
    code_data = cache.get(cache_key)
    urlprefix = None
    if assign_type == AssignType.Inner:
        urlprefix = CompanyService.get_company().get('urlprefix', '')
    if urlprefix is None:
        urlprefix = ''
    if code_data is not None:
        return code_data
    ret = BatchService.get_batch_code(batch_id, assign_type, section_id, -1)
    if ret is not None and ret['code'] == 0:
        code_data = ret['data']
        code_data['code'] = '\n'.join([urlprefix.strip() + c.strip() for c in ret['data']['code']])
        cache.set(cache_key, code_data, cache_expires_in)
    return code_data


def __get_assign_type(code_type):
    if code_type == 'inner':
        return AssignType.Inner
    elif code_type == 'outer':
        return AssignType.Outer
    else:
        return AssignType.Case


def __generate_key(feature):
    return 'batch_code_' + str(feature)


def __generate_csv_file_for_code(code_data):
    filename = '%d_%d_%d.csv' % (code_data['batchId'], code_data['assignType'], code_data['sectionId'])
    csvfile = StringIO.StringIO()
    csvfile.write(code_data['code'])
    response = HttpResponse(csvfile.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response['Content-Length'] = csvfile.tell()
    csvfile.seek(0)
    return response


def set_index(request):
    subject = Subject.get_instance(request.session)
    user = subject.get_user_info()
    user_id = None if subject.has_role('root') else user.get("id")

    base_data = {
        'app_name': u'生产赋码',
        'page_name': CompanyService.get_company().get('name'),
        'page_desc': u'批次管理',
        'product_options': [],
        'factory_options': [],
        'products': []
    }
    products = ProductService.get_product_list(created_by=user_id)
    product_dict = {}
    if products and products['code'] == 0:
        for product in products['data']:
            id = product['id']
            base_data['product_options'].append(
                {'text': product['name'], 'value': id}
            )
            base_data['products'].append(product)
            product_dict[id] = product
    factories = FactoryService.get_factory_list(created_by=user_id)
    if factories and factories['code'] == 0:
        for factory in factories['data']:
            base_data['factory_options'].append({'text': factory['factoryName'], 'value': factory['id']})
    base_data['batch_list'] = set_batch_list(BatchService.get_batch_list(created_by=user_id), product_dict)
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
        product_id=body.get('product_id'),
        expired_time=body.get('expired_time'),
        product_info=body.get('product_info'),
        callback_uri=body.get('callback_uri'),
        created_by=user['id'],
        updated_by=user['id']
    )


def get_factory_by_id(factory_id):
    if factory_id is None:
        return None
    if factory_id < 0:
        return '-'
    response = FactoryService.get_factory(factory_id=factory_id)
    if response is not None and response['code'] == 0:
        return response['data'].get('factoryName')
    else:
        print 'get factory info failed:', json.dumps(response)
        return None


def set_batch_list(response, product_dict):
    batch_list = []
    for b in response['data']:
        product_info = product_dict.get(b['productId'], {})
        batch_list.append({
            'expired_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(b['updatedTime'] / 1000)),
            'product_name': product_info.get('name'),
            'barcode': b['barcode'],
            'unit_count': '%d%s' % (b['unitCount'], product_info.get('unit')),
            'inner_code_factory_id': b['incodeFactory'],
            'inner_code_factory': get_factory_by_id(b['incodeFactory']),
            'outer_code_factory_id': b['outcodeFactory'],
            'outer_code_factory': get_factory_by_id(b['outcodeFactory']),
            'case_code_factory_id': b['casecodeFactory'],
            'case_code_factory': get_factory_by_id(b['casecodeFactory']),
            'code_type_count': int(b['incodeFactory'] is not None) + int(b['outcodeFactory'] is not None) + int(
                b['casecodeFactory'] is not None),
            'enabled_factory_id': b['factoryId'],
            'enabled_factory': get_factory_by_id(b['factoryId']),
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
        subject = Subject.get_instance(request.session)
        user = subject.get_user_info()
        user_id = None if subject.has_role('root') else user.get("id")
        response = BatchService.get_batch_list(created_by=user_id)
        return JsonResponse(response)


def batch_by_id(request, batch_id):
    if request.method == 'GET':
        response = BatchService.get_batch(batch_id)
        return JsonResponse(response)


def batch_send_code(request):
    if request.method == 'POST':
        batch_id = request.POST.get('batch_id')
        factory_id = request.POST.get('factory_id')
        batch_info_resp = BatchService.get_batch(batch_id)
        if batch_info_resp is None or batch_info_resp['code'] != 0:
            return JsonResponse({'code': -1, 'msg': 'batch not found'})
        batch_info = batch_info_resp['data']
        if batch_info.get('status') != BatchStatus.Ready:
            # batch is not ready
            print 'batch status is not ready:', batch_info.get('status')
            return JsonResponse({'code': -1, 'msg': 'batch status is not ready'})
        else:
            ret = BatchService.update_batch_secret_status_and_send_to_factory_owner(batch_id, factory_id)
            if ret is None:
                ret = {'code': -1, 'msg': 'send secret failed'}
            return JsonResponse(ret)


def batch_download_code(request):
    if request.method == 'POST':
        code_type = request.POST.get('code_type')
        batch_id = request.POST.get('batch_id')
        csv_type = (request.POST.get('csv_type') == 'true')
        assign_type = __get_assign_type(code_type)
        code_data = __get_batch_code(batch_id, assign_type, 0)
        if code_data is None:
            return JsonResponse({'code': -1, 'msg': 'download failed'})
        else:
            return __generate_csv_file_for_code(code_data) if csv_type is True else ResponseEntity.ok(
                code_data['code'].split('\n'))


def batch_enable_code(request):
    if request.method == 'POST':
        batch_id = request.POST.get('batch_id')
        factory_id = request.POST.get('factory_id')
        timestamp = utils.current_timestamp_in_millis()
        batch_info_resp = BatchService.get_batch(batch_id)
        if batch_info_resp is None or batch_info_resp['code'] != 0:
            print 'batch not found:', batch_id
            return JsonResponse({'code': -1, 'msg': 'batch not found'})
        batch_info = batch_info_resp['data']
        enable_casecode = batch_info['casecodeFactory'] is not None
        enable_incode = batch_info['incodeFactory'] is not None
        enable_outcode = batch_info['outcodeFactory'] is not None
        code_count = int(enable_incode) + int(enable_outcode) + int(enable_casecode)
        if batch_info.get('status') != BatchStatus.Ready:
            # batch is not ready
            print 'batch status is not ready:', batch_info.get('status')
            return JsonResponse({'code': -1, 'msg': 'batch status is not ready'})
        elif code_count > 1 or enable_casecode:
            print 'unable to enable code batchly since either there are more than code type or there is case code'
            return JsonResponse({'code': -1, 'msg': 'more than one type of code in the batch'})
        else:
            if enable_incode:
                assign_type = AssignType.Inner
            else:
                assign_type = AssignType.Outer
            ret = BatchService.activate_batch_code(batch_id=batch_id,
                                                   assign_type=assign_type,
                                                   enabled_time=timestamp,
                                                   enabled_factory=factory_id)
            if ret is None or ret['code'] != 0:
                return JsonResponse({'code': -1, 'msg': 'enable code failed'})
            BatchService.update_batch_status(batch_id=batch_id, status=BatchStatus.Done)
            return JsonResponse(ret)
