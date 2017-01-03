import requests
from django.http import JsonResponse

# Create your views here.
server_url = 'http://api.wemarklinks.net:81'


def batch(request):
	pass


def factory(request):
	if request.method == 'GET':
		response = get_factory()
		return JsonResponse(response)
	elif request.method == 'POST':
		pass


def get_factory():
	return requests.get('%s/factory' % server_url).json()

