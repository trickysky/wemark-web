from wemark_config import SERVER_HOST
import utils
import requests
from s.models import CompanyInfo


class FactoryService(object):
    @staticmethod
    def get_factory_list(factory_name=None, location=None, region=None, f_type=None, status=None, created_by=None,
                         updated_by=None):
        params = {
            'factory_name': factory_name,
            'location': location,
            'region': region,
            'type': f_type,
            'status': status,
            'created_by': created_by,
            'updated_by': updated_by
        }
        params = utils.clean_params(params)
        r = requests.get('%s/factory/info' % SERVER_HOST, params=params)
        return r.json() if r.ok else None

    @staticmethod
    def get_factory(factory_id):
        return requests.get('%s/factory/info/%s' % (SERVER_HOST, factory_id)).json()

    @staticmethod
    def create_factory_and_secret(status, created_by, updated_by, factory_name='', location='', region='', f_type='',
                                  owner='', owner_email='', owner_mobile=''):
        params = {
            'factory_name': factory_name,
            'location': location,
            'region': region,
            'type': f_type,
            'owner': owner,
            'owner_email': owner_email,
            'owner_mobile': owner_mobile,
            'status': status,
            'created_by': created_by,
            'updated_by': updated_by,
            'created_time': utils.current_timestamp_in_millis(),
            'updated_time': utils.current_timestamp_in_millis()
        }
        params = utils.clean_params(params)
        r = requests.post('%s/factory' % SERVER_HOST, params=params)
        return r.json() if r.ok else None

    @staticmethod
    def create_factory(status, created_by, updated_by, factory_name='', location='', region='', f_type='', owner='',
                       owner_email='', owner_mobile=''):
        params = {
            'factory_name': factory_name,
            'location': location,
            'region': region,
            'type': f_type,
            'owner': owner,
            'owner_email': owner_email,
            'owner_mobile': owner_mobile,
            'status': status,
            'created_by': created_by,
            'updated_by': updated_by,
            'created_time': utils.current_timestamp_in_millis(),
            'updated_time': utils.current_timestamp_in_millis()
        }
        params = utils.clean_params(params)
        r = requests.post('%s/factory/info' % SERVER_HOST, params=params)
        return r.json() if r.ok else None

    @staticmethod
    def update_factory(factory_id, factory_name=None, location=None, region=None, f_type=None, owner=None,
                       owner_email=None, owner_mobile=None, status=None, updated_by=None):
        params = {
            'factory_name': factory_name,
            'location': location,
            'region': region,
            'type': f_type,
            'owner': owner,
            'owner_email': owner_email,
            'owner_mobile': owner_mobile,
            'status': status,
            'updated_by': updated_by,
            'updated_time': utils.current_timestamp_in_millis()
        }
        params = utils.clean_params(params)
        r = requests.put('%s/factory/info/%s' % (SERVER_HOST, factory_id), data=params)
        return r.json() if r.ok else None

    @staticmethod
    def delete_factory(factory_id):
        r = requests.delete('%s/factory/info/%s' % (SERVER_HOST, factory_id))
        return r.json() if r.ok else None

    @staticmethod
    def create_factory_secret(factory_id, factory_secret):
        params = {
            'factory_id': factory_id,
            'secret': factory_secret,
            'created_time': utils.current_timestamp_in_millis(),
            'updated_time': utils.current_timestamp_in_millis()
        }
        params = utils.clean_params(params)
        r = requests.post('%s/factory/secret' % SERVER_HOST, params=params)
        return r.json() if r.ok else None

    @staticmethod
    def get_factory_secret(factory_id):
        r = requests.get('%s/factory/secret/%s' % (SERVER_HOST, factory_id))
        return r.json() if r.ok else None

    @staticmethod
    def update_factory_secret(secret_id, factory_id=None, factory_secret=None):
        params = {
            'factory_id': factory_id,
            'secret': factory_secret,
            'updated_time': utils.current_timestamp_in_millis()
        }
        params = utils.clean_params(params)
        r = requests.put('%s/factory/secret/%s' % (SERVER_HOST, secret_id), params=params)
        return r.json() if r.ok else None

    @staticmethod
    def delete_factory_secret(secret_id):
        r = requests.delete('%s/factory/secret/%s' % (SERVER_HOST, secret_id))
        return r.json() if r.ok else None


class BatchService(object):
    @staticmethod
    def get_batch_list(factory_id=None, incode_factory=None, outcode_factory=None, casecode_factory=None,
                       case_size=None, barcode=None, status=None, created_by=None, start_time=None, end_time=None):
        params = {
            'factory_id': factory_id,
            'incode_factory': incode_factory,
            'outcode_factory': outcode_factory,
            'casecode_factory': casecode_factory,
            'case_size': case_size,
            'barcode': barcode,
            'status': status,
            'created_by': created_by,
            'start_time': start_time,
            'end_time': end_time
        }
        params = utils.clean_params(params)
        r = requests.get('%s/batch' % SERVER_HOST, params=params)
        return r.json() if r.ok else None

    @staticmethod
    def get_batch(batch_id):
        r = requests.get('%s/batch/info/%s' % (SERVER_HOST, batch_id))
        return r.json() if r.ok else None

    @staticmethod
    def create_batch(factory_id, product_id, incode_factory, outcode_factory, casecode_factory, case_count, case_size, unit_count,
                     barcode, expired_time, product_info, callback_uri, created_by, updated_by):
        params = {
            'factory_id': factory_id,
            'product_id': product_id,
            'incode_factory': incode_factory,
            'outcode_factory': outcode_factory,
            'casecode_factory': casecode_factory,
            'case_count': case_count,
            'case_size': case_size,
            'unit_count': unit_count,
            'barcode': barcode,
            'expired_time': expired_time,
            'product_info': product_info,
            'callback_uri': callback_uri,
            'created_by': created_by,
            'created_time': utils.current_timestamp_in_millis(),
            'updated_by': updated_by,
            'updated_time': utils.current_timestamp_in_millis()
        }
        params = utils.clean_params(params)
        r = requests.post('%s/batch' % SERVER_HOST, data=params)
        return r.json() if r.ok else None

    @staticmethod
    def update_batch_status(batch_id, status):
        params = {
            'status': status
        }
        params = utils.clean_params(params)
        r = requests.put('%s/batch/%s/status' % (SERVER_HOST, batch_id), params=params)
        return r.json() if r.ok else None

    @staticmethod
    def get_batch_secret_status(batch_id):
        r = requests.get('%s/batch/%s/secret_status' % (SERVER_HOST, batch_id))
        return r.json() if r.ok else None

    @staticmethod
    def update_batch_secret_status_and_send_to_factory_owner(batch_id, factory_id):
        params = {
            'factory_id': factory_id
        }
        params = utils.clean_params(params)
        r = requests.put('%s/batch/%s/secret' % (SERVER_HOST, batch_id), params=params)
        return r.json() if r.ok else None

    @staticmethod
    def get_batch_section_count(batch_id, assign_type, factory_id):
        params = {
            'assign_type': assign_type,
            'factory_id': factory_id
        }
        params = utils.clean_params(params)
        r = requests.get('%s/batch/%s/code_section_count' % (SERVER_HOST, batch_id), params=params)
        return r.json() if r.ok else None

    @staticmethod
    def get_batch_code(batch_id, assign_type, section_id, factory_id):
        params = {
            'assign_type': assign_type,
            'section_id': section_id,
            'factory_id': factory_id
        }
        params = utils.clean_params(params)
        r = requests.get('%s/batch/%s/code' % (SERVER_HOST, batch_id), params=params)
        return r.json() if r.ok else None

    @staticmethod
    def activate_batch_code(batch_id, enabled_time, enabled_factory):
        params = {
            'enabled_time': enabled_time,
            'enabled_factory': enabled_factory
        }
        params = utils.clean_params(params)
        r = requests.put('%s/batch/%s/enable_code' % (SERVER_HOST, batch_id), params=params)
        return r.json() if r.ok else None


class CompanyService(object):
    @staticmethod
    def get_company():
        company_count = CompanyInfo.objects.all().count()
        company_info = CompanyInfo.objects.get() if company_count else None
        return {
            'name': company_info.name if company_info else None,
            'description': company_info.description if company_info else None,
            'homepage': company_info.homepage if company_info else None,
        }

    @staticmethod
    def update_company(name=None, description=None, homepage=None):
        try:
            company_count = CompanyInfo.objects.all().count()
            if not 0 == company_count:
                CompanyInfo.objects.all().delete()
            company_info = CompanyInfo(name=name, description=description, homepage=homepage)
            company_info.save()
            return {
                'code': 0,
                'msg': 'update company info complete'
            }
        except Exception as e:
            return {
                'code': 1,
                'msg': 'update company info error:\r\n %s' % e
            }


class ProductService(object):
    @staticmethod
    def get_product_list(name=None, barcode=None, intro=None, status=None, created_by=None, updated_by=None):
        params = {
            'name': name,
            'barcode': barcode,
            'intro': intro,
            'status': status,
            'created_by': created_by,
            'updated_by': updated_by
        }
        params = utils.clean_params(params)
        r = requests.get('%s/product' % SERVER_HOST, params=params)
        return r.json() if r else None

    @staticmethod
    def new_product(name=None, status=0, created_by=None, updated_by=None, barcode=None, intro=None, icon=None,
                    images=None, description=None):
        params = {
            'name': name,
            'status': status,
            'created_by': created_by,
            'created_time': utils.current_timestamp_in_millis(),
            'updated_by': updated_by,
            'updated_time': utils.current_timestamp_in_millis(),
            'barcode': barcode,
            'intro': intro,
            'icon': icon,
            'images': images,
            'description': description
        }
        params = utils.clean_params(params)
        r = requests.post('%s/product' % SERVER_HOST, data=params)
        return r.json() if r else None

    @staticmethod
    def get_product(product_id=None):
        if product_id:
            r = requests.get('%s/product/%s' % (SERVER_HOST, product_id))
            return r.json() if r else None
        else:
            return None

    @staticmethod
    def update_product(product_id=None, name=None, status=0, updated_by=None, barcode=None, intro=None, icon=None,
                       images=None, description=None):
        if product_id:
            params = {
                'name': name,
                'status': status,
                'updated_by': updated_by,
                'updated_time': utils.current_timestamp_in_millis(),
                'barcode': barcode,
                'intro': intro,
                'icon': icon,
                'images': images,
                'description': description
            }
            params = utils.clean_params(params)
            r = requests.put('%s/product/%s' % (SERVER_HOST, product_id), data=params)
            return r.json() if r.ok else None
        else:
            return None

    @staticmethod
    def delete_product(product_id):
        if product_id:
            r = requests.delete('%s/product/%s' % (SERVER_HOST, product_id))
            return r.json() if r.ok else None
        else:
            return None


class DataService(object):
    @staticmethod
    def get_scan_code_list(batch_id, code=None, code_type=None, function=None, user_code=None, user_type=None,
                           location=None, scan_times=None, min_times=None, max_times=None, start_time=None,
                           end_time=None, order_by=None, offset=None, max_count=None):
        params = {
            'batch_id': batch_id,
            'code': code,
            'code_type': code_type,
            'function': function,
            'user_code': user_code,
            'user_type': user_type,
            'location': location,
            'scan_times': scan_times,
            'min_times': min_times,
            'max_times': max_times,
            'start_time': start_time,
            'end_time': end_time,
            'order_by': order_by,
            'offset': offset,
            'max_count': max_count
        }
        params = utils.clean_params(params)
        r = requests.get('%s/data/scan' % SERVER_HOST, params=params)
        return r.json() if r.ok else None

    @staticmethod
    def get_award_list(batch_id, code=None, code_type=None, user_code=None, user_type=None, start_time=None,
                       end_time=None, location=None, start_accept_time=None, end_accept_time=None, accept_location=None,
                       order_by=None, offset=None, max_count=None):
        params = {
            'batch_id': batch_id,
            'code': code,
            'code_type': code_type,
            'user_code': user_code,
            'user_type': user_type,
            'start_time': start_time,
            'end_time': end_time,
            'location': location,
            'start_accept_time': start_accept_time,
            'end_accept_time': end_accept_time,
            'accept_location': accept_location,
            'order_by': order_by,
            'offset': offset,
            'max_count': max_count
        }
        params = utils.clean_params(params)
        r = requests.get('%s/data/award' % SERVER_HOST, params=params)
        return r.json() if r.ok else None

    @staticmethod
    def get_batch_list(barcode=None, factory_id=None, incode_factory=None, outcode_factory=None, casecode_factory=None,
                       case_count=None, min_case_count=None, max_case_count=None, case_size=None, unit_count=None,
                       min_unit_count=None, max_unit_count=None, created_by=None, start_expired_time=None,
                       end_expired_time=None, start_created_time=None, end_created_time=None, status=None,
                       order_by=None, offset=None, max_count=None):
        params = {
            'barcode': barcode,
            'factory_id': factory_id,
            'incode_factory': incode_factory,
            'outcode_factory': outcode_factory,
            'casecode_factory': casecode_factory,
            'case_count': case_count,
            'min_case_count': min_case_count,
            'max_case_count': max_case_count,
            'case_size': case_size,
            'unit_count': unit_count,
            'min_unit_count': min_unit_count,
            'max_unit_count': max_unit_count,
            'created_by': created_by,
            'start_expired_time': start_expired_time,
            'end_expired_time': end_expired_time,
            'start_created_time': start_created_time,
            'end_created_time': end_created_time,
            'status': status,
            'order_by': order_by,
            'offset': offset,
            'max_count': max_count
        }
        params = utils.clean_params(params)
        r = requests.get('%s/data/batch' % SERVER_HOST, params=params)
        return r.json() if r.ok else None

    @staticmethod
    def get_associated_code_count(batch_id, assign_type=None, enabled=None, enabled_factory=None):
        params = {
            'batch_id': batch_id,
            'assign_type': assign_type,
            'enabled': enabled,
            'enabled_factory': enabled_factory
        }
        params = utils.clean_params(params)
        r = requests.get('%s/data/associate/count' % SERVER_HOST, params=params)
        return r.json() if r.ok else None
