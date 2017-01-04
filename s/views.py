import requests
from django.http import JsonResponse
from wemark_config import SERVER_HOST
import time
# Create your views here.


def batch(request):
	pass


def factory(request):
	if request.method == 'GET':
		response = get_factory()
		return JsonResponse(response)
	elif request.method == 'POST':
		return new_factory(request)


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

