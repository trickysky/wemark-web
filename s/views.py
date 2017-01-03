import requests
from django.http import JsonResponse
from wemark_config import SERVER_HOST
# Create your views here.


def batch(request):
	pass


def factory(request):
	if request.method == 'GET':
		response = get_factory()
		return JsonResponse(response)
	elif request.method == 'POST':
		pass


def get_factory():
	return requests.get('%s/factory' % SERVER_HOST).json()

