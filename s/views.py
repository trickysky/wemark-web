import requests
from django.http import JsonResponse
from wemark_config import SERVER_HOST
import time
from django.http import QueryDict
# Create your views here.


def batch(request):
	pass


def factory(request):
	if request.method == 'GET':
		response = get_factory()
		return JsonResponse(response)
	elif request.method == 'POST':
		return new_factory(request)


def factory_info(request, factory_id):
	if request.method == 'DELETE':
		return JsonResponse(requests.delete('%s/factory/info/%s' % (SERVER_HOST, factory_id)).json())
	if request.method == 'PUT':
		return JsonResponse(update_factory(request, factory_id))


def get_factory():
	return requests.get('%s/factory/info' % SERVER_HOST).json()


def new_factory(request):
	body = request.POST
	params = {
		'factory_name': body.get('factory_name'),
		'location': body.get('location'),
		'region': body.get('region'),
		'type': body.get('type'),
		'owner': body.get('owner'),
		'owner_email': body.get('owner_email'),
		'owner_mobile': body.get('owner_mobile'),
		'status': body.get('status'),
		'created_time': int(time.time()) * 1000,
		'updated_time': int(time.time()) * 1000
	}
	response = requests.post('%s/factory' % SERVER_HOST, data=params).json()
	return JsonResponse(response)


def update_factory(request, factory_id):
	body = request.POST
	b = request.GET
	params = {
		'factory_name': body.get('factory_name'),
		'location': body.get('location'),
		'region': body.get('region'),
		'type': body.get('type'),
		'owner': body.get('owner'),
		'owner_email': body.get('owner_email'),
		'owner_mobile': body.get('owner_mobile'),
		'status': body.get('status'),
		'updated_time': int(time.time()) * 1000
	}
	response = requests.put('%s/factory/info/%s' % (SERVER_HOST, factory_id), data=params).json()
	return JsonResponse(response)
