from django.http import JsonResponse

from wemark.commons.services import FactoryService, CompanyService, ProductService, AwardSettingService
from oauth2.commons.security import Subject
from wemark.commons.response import ResponseEntity


# Create your views here.


def batch(request):
    pass


def factory(request):
    r = None
    info = get_user_info(request)
    if request.method == 'GET':
        r = FactoryService.get_factory_list(created_by=info.get('id'))
    if request.method == 'POST':
        body = request.POST
        r = FactoryService.create_factory(
            factory_name=body.get('factory_name'),
            location=body.get('location'),
            region=body.get('region'),
            f_type=body.get('type'),
            owner=body.get('owner'),
            owner_email=body.get('owner_email'),
            owner_mobile=body.get('owner_mobile'),
            status=body.get('status'),
            created_by=info['id'],
            updated_by=info['id']
        )
    return JsonResponse(r) if r else ResponseEntity.server_error()


def factory_by_id(request, factory_id):
    r = None
    if request.method == 'DELETE':
        r = FactoryService.delete_factory(
            factory_id=factory_id
        )
    if request.method == 'POST':
        info = get_user_info(request)
        body = request.POST
        r = FactoryService.update_factory(
            factory_id=factory_id,
            factory_name=body.get('factory_name'),
            location=body.get('location'),
            region=body.get('region'),
            f_type=body.get('type'),
            owner=body.get('owner'),
            owner_email=body.get('owner_email'),
            owner_mobile=body.get('owner_mobile'),
            status=body.get('status'),
            updated_by=info['id']
        )
    return JsonResponse(r) if r else ResponseEntity.server_error()


def get_user_info(request):
    subject = Subject.get_instance(request.session)
    return subject.get_user_info()


def company(request):
    if request.method == 'POST':
        body = request.POST
        r = CompanyService.update_company(
            name=body.get('name'),
            description=body.get('description'),
            homepage=body.get('homepage'),
        )
        return JsonResponse(r)


def product(request):
    if request.method == 'POST':
        body = request.POST
        info = get_user_info(request)
        r = ProductService.new_product(
            name=body.get('name'),
            unit=body.get('unit'),
            created_by=info['id'],
            updated_by=info['id'],
            barcode=body.get('barcode'),
            intro=body.get('intro'),
            icon=body.get('icon'),
            images=body.get('images'),
            description=body.get('description'),
        )
        return JsonResponse(r) if r else ResponseEntity.server_error()


def product_by_id(request, product_id):
    r = None
    if request.method == 'DELETE':
        r = ProductService.delete_product(
            product_id=product_id
        )
    elif request.method == 'POST':
        body = request.POST
        info = get_user_info(request)
        r = ProductService.update_product(
            product_id=product_id,
            name=body.get('name'),
            icon=body.get('icon'),
            images=body.get('images'),
            intro=body.get('intro'),
            description=body.get('description'),
            updated_by=info['id']
        )
    elif request.method == 'GET':
        r = ProductService.get_product(product_id)
    return JsonResponse(r) if r else ResponseEntity.server_error()


def award(request):
    if request.method == 'POST':
        body = request.POST
        r = AwardSettingService.update_award_setting(
            total_prize=float(body.get('total_prize')),
            award_rate=float(body.get('award_rate')),
            min_prize=float(body.get('min_prize')),
            max_prize=float(body.get('max_prize'))
        )
        return JsonResponse(r)