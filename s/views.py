from django.http import JsonResponse, QueryDict

from wemark.commons.services import FactoryService, CompanyService
from oauth2.commons.security import Subject


# Create your views here.


def batch(request):
	pass


def factory(request):
	r = None
	if request.method == 'GET':
		r = FactoryService.get_factory_list()
	if request.method == 'POST':
		info = get_user_info(request)
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
	return JsonResponse(r)


def factory_id(request, factory_id):
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
	return JsonResponse(r)


def get_user_info(request):
	subject = Subject.get_instance(request.session)
	info = subject.get_user_info()
	if info is None:
		info = subject.get_user_info(True)
	return info


def company(request):
	if request.method == 'POST':
		body = request.POST
		r = CompanyService.update_company(
			name=body.get('name'),
			description=body.get('description'),
			homepage=body.get('homepage'),
		)
		return JsonResponse(r)
