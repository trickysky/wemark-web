from wemark_config import SERVER_HOST
from django.http import JsonResponse
import utils
import requests


class FactoryService(object):
    @staticmethod
    def get_factory_list():
        return requests.get('%s/factory/info' % SERVER_HOST).json()

    @staticmethod
    def get_factory(factory_id):
        r = requests.get('%s/factory/info/%s' % (SERVER_HOST, factory_id)).json()
        return JsonResponse(r)

    @staticmethod
    def create_factory(factory_name, location, region, f_type, owner, owner_email, owner_mobile, status):
        params = {
            'factory_name': factory_name,
            'location': location,
            'region': region,
            'type': f_type,
            'owner': owner,
            'owner_email': owner_email,
            'owner_mobile': owner_mobile,
            'status': status,
            'created_time': utils.current_timestamp_in_millis(),
            'updated_time': utils.current_timestamp_in_millis()
        }
        r = requests.post('%s/factory' % SERVER_HOST, data=params).json()
        return JsonResponse(r)

    @staticmethod
    def update_factory(factory_id, factory_name, location, region, f_type, owner, owner_email, owner_mobile, status):
        params = {
            'factory_name': factory_name,
            'location': location,
            'region': region,
            'type': f_type,
            'owner': owner,
            'owner_email': owner_email,
            'owner_mobile': owner_mobile,
            'status': status,
            'updated_time': utils.current_timestamp_in_millis()
        }

        r = requests.put('%s/factory/info/%s' % (SERVER_HOST, factory_id), data=params).json()
        return JsonResponse(r)

    @staticmethod
    def delete_factory(factory_id):
        r = requests.delete('%s/factory/info/%s' % (SERVER_HOST, factory_id)).json()
        return JsonResponse(r)


class BatchService(object):
    pass
