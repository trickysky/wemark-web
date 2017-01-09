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
		return requests.get('%s/factory/info' % SERVER_HOST, params=params).json()

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
		return requests.post('%s/factory' % SERVER_HOST, params=params).json()

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
		return requests.post('%s/factory/info' % SERVER_HOST, params=params).json()

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
		return requests.put('%s/factory/info/%s' % (SERVER_HOST, factory_id), data=params).json()

	@staticmethod
	def delete_factory(factory_id):
		return requests.delete('%s/factory/info/%s' % (SERVER_HOST, factory_id)).json()

	@staticmethod
	def create_factory_secret(factory_id, factory_secret):
		params = {
			'factory_id': factory_id,
			'secret': factory_secret,
			'created_time': utils.current_timestamp_in_millis(),
			'updated_time': utils.current_timestamp_in_millis()
		}
		params = utils.clean_params(params)
		return requests.post('%s/factory/secret' % SERVER_HOST, params=params).json()

	@staticmethod
	def get_factory_secret(factory_id):
		return requests.get('%s/factory/secret/%s' % (SERVER_HOST, factory_id)).json()

	@staticmethod
	def update_factory_secret(secret_id, factory_id=None, factory_secret=None):
		params = {
			'factory_id': factory_id,
			'secret': factory_secret,
			'updated_time': utils.current_timestamp_in_millis()
		}
		params = utils.clean_params(params)
		return requests.put('%s/factory/secret/%s' % (SERVER_HOST, secret_id), params=params).json()

	@staticmethod
	def delete_factory_secret(secret_id):
		return requests.delete('%s/factory/secret/%s' % (SERVER_HOST, secret_id)).json()


class BatchService(object):
	@staticmethod
	def get_batch_list():
		return requests.get('%s/batch' % SERVER_HOST).json()

	@staticmethod
	def create_batch(factory_id, incode_factory, outcode_factory, casecode_factory, case_count, case_size, unit_count,
	                 barcode, expired_time, product_info, callback_uri):
		params = {
			'factory_id': factory_id,
			'incode_factory': incode_factory,
			'outcode_factory': outcode_factory,
			'casecode_factory': casecode_factory,
			'case_count': case_count,
			'case_size': case_size,
			'unit_count': unit_count,
			'barcode': barcode,
			'expired_time': expired_time,
			'product_info': product_info,
			'callback_uri': callback_uri
		}
		params = utils.clean_params(params)
		return requests.post('%s/batch' % SERVER_HOST, data=params).json()


class CompanyService(object):
	@staticmethod
	def get_company():
		company_count = CompanyInfo.objects.all().count()
		conpany_info = CompanyInfo.objects.get() if company_count else None
		return {
			'name': conpany_info.name if conpany_info else None,
			'description': conpany_info.description if conpany_info else None,
			'homepage': conpany_info.homepage if conpany_info else None,
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
	def get_product_list():
		r = requests.get('%s/product' % SERVER_HOST)
		return r.json() if r else None

	@staticmethod
	def new_product(name=None, status=-1, created_by=None, updated_by=None, barcode=None, intro=None, icon=None,
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
		r = requests.post('%s/product' % SERVER_HOST, data=params).json()
		return r.json() if r else None

	@staticmethod
	def get_product(product_id=None):
		if product_id:
			r = requests.get('%s/product/%s' % (SERVER_HOST, product_id))
			return r.json() if r else None
		else:
			return None

	@staticmethod
	def update_product(product_id=None, name=None, status=-1, updated_by=None, barcode=None, intro=None, icon=None,
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
			return r.json() if r else None
		else:
			return None

	@staticmethod
	def delete_product(product_id):
		if product_id:
			r = requests.delete('%s/product/%s' % (SERVER_HOST, product_id))
			return r.json() if r else None
		else:
			return None
