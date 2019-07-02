import re
import os
import json
import mimetypes
import base64
import requests

from myroductivitytool.common.models import *
from myroductivitytool.common.serializers import *
from myroductivitytool.common.utils import CommonUtils

from django.utils import timezone
from datetime import datetime, timedelta, date
from django.conf.urls.static import static
from django.http import HttpResponse
from django.conf import settings
from urllib.parse import urlparse
from django.core.paginator import Paginator


class ModelService(object):

	ALLOWED_ACTIONS_FOR_GET = [
		'view', 
		'count', 
		'get_context',
		'view_multiple',
		'get_filter_context'
	]
	
	ALLOWED_ACTIONS_FOR_POST = [
		'add', 
		'update', 
		'delete'
	]

	# It should never be used direclty from view, only service methods can use it.
	@classmethod
	def base_filter_service(cls, **kwargs):

		try:
			filter_query = kwargs.get('filter_query', dict())
			exclude_query = kwargs.get('exclude_query', None)
			results = cls.entity.objects.filter(**filter_query)

			if exclude_query:
				results = results.exclude(**exclude_query)

			return results
		except Exception as e:
			print(e)
			return list()

	@classmethod
	def view_multiple(cls, **kwargs):
		try:
			results = cls.base_filter_service(**kwargs)
			page_query = kwargs.get('page_query', dict())

			if not page_query:
				return {'success': True, 'results': cls.entity_serializer(results, many=True).data}
				
			service_response = cls.get_page_data(**{'page_query': page_query, 'results': results})

			if not service_response.get('success', False):
				return service_response
			else:
				results = cls.entity_serializer(service_response.get('results'), many=True).data
				return service_response.update({
					'results': results
				})

		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not fetch {0}'.format(cls.entity_name)}

	@classmethod
	def view(cls ,**kwargs):
		try:

			results = cls.base_filter_service(**kwargs)
			if results:
				return {'success': True, 'result': cls.entity_serializer(results[0]).data}
			else:
				return {'success': False, 'message': 'We could not find the {0}'.format(cls.entity_name)}

		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not fetch {0}'.format(cls.entity_name)}

	@classmethod
	def count(cls, **kwargs):
		try:
			count = cls.base_filter_service(**kwargs).count()
			return {'success': True, 'count': count}
		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not count the number of {0}'.format(cls.entity_name)}

	@classmethod
	def get_context(cls, **kwargs):
		try:
			context = dict()
			instance_id = kwargs.get('instance_id', None)
			if instance_id:
				instance = cls.entity.objects.get(id=instance_id)
				instance = cls.entity_serializer(instance).data
				context.update({
					'instance': instance
				})
			
			return {'success': True, 'context': context}
		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not fetch context for {0}'.format(cls.entity_name)}

	@classmethod
	def get_filter_context(cls, **kwargs):
		try:
			context = dict()
	
			return {'success': True, 'context': context}
		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not fetch filter context for {0}'.format(cls.entity_name)}

	@classmethod
	def construct_filter_query(cls, **kwargs):

		try:
			filter_query = dict()
			if not hasattr(cls, 'entity_field_to_query_map'):
				return {'success': True, 'filter_query': filter_query}

			for key, value in kwargs.items():
				if not value:
					continue
				if cls.entity_field_to_query_map.get(key, None):
					query_data = cls.entity_field_to_query_map.get(key)
					if query_data.get('data_type') == 'boolean':
						if value == 'yes':
							value = True
						else:
							value = False
					elif query_data.get('data_type') == 'list':
						value = value.strip('[').strip(']').split(',')
					filter_query.update({query_data.get('field'): value})

			return {'success': True, 'filter_query': filter_query}

		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not filter {0}'.format(cls.entity_name)}

	@classmethod
	def construct_page_query(cls, **kwargs):

		try:
			page_query = dict()
			page_no = kwargs.get('pageNo', None)
			page_items = kwargs.get('pageItems', None)

			if page_no and page_items:
				page_query.update({
					'page_no': int(page_no),
					'page_items': int(page_items)
				})
			return {'success': True, 'page_query': page_query}

		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not fetch {0}'.format(cls.entity_name)}

	@classmethod
	def validate_entity_identifiers(cls, **kwargs):
		try:
			error_messages = list()
			success = True
			instance = kwargs.get('instance')
			entity_data = kwargs.get('entity_data', dict())
			if not cls.entity_identifiers:
				return {'success': True, 'message': '{0} validated'}

			for key, value in cls.entity_identifiers.items():
				if entity_data[key] != getattr(instance, key):
					error_messages.append('{0} can not be updated for existing {1}'.format(value, cls.entity_name))

			if error_messages:
				success = False
			return {'success': success, 'messages': error_messages}

		except Exception as e:
			print(e)
			return {'success': False, 'messages': ['We could not validate the entity identifiers']}

	@classmethod
	def get_page_data(cls, **kwargs):

		try:
			results = kwargs.get('results', list())
			page_query = kwargs.get('page_query', dict())

			page_no = int(page_query.get('pageNo', 1))

			if not page_query.get('pageItems', None):
				return {'success': False, 'message': 'Number of items per page is missing'}

			page_items = int(page_query.get('pageItems'))

			paginator = Paginator(results, page_items)
			total_pages = paginator.num_pages
			page = paginator.page(page_no)
			page_data = page.object_list

			return {'success': True, 'results': page_data, 'total_pages': total_pages, 'page_no': page_no}

		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not paginate {0} data'.format(cls.entity_name)}




class BaseModelService(ModelService):

	ALLOWED_ACTIONS_FOR_GET = [
		'view', 
		'get_context', 
		'count_active', 
		'view_active_multiple',
		'count_deleted',
		'view_deleted_multiple',
		'get_filter_context'
	]
	
	ALLOWED_ACTIONS_FOR_POST = [
		'add', 
		'update', 
		'delete'
	]

	entity_field_to_query_map = {
		'isDeleted': {'field': 'is_deleted', 'data_type': 'boolean'}
	}

	@classmethod
	def count_active(cls, **kwargs):
		filter_query = kwargs.get('filter_query', dict())
		filter_query.update({
			'is_deleted': False
		})
		kwargs.update({
			'filter_query': filter_query
		})
		return cls.count(**kwargs)

	@classmethod
	def view_active_multiple(cls, **kwargs):
		filter_query = kwargs.get('filter_query', dict())
		filter_query.update({
			'is_deleted': False
		})
		kwargs.update({
			'filter_query': filter_query
		})
		return cls.view_multiple(**kwargs)

	@classmethod
	def count_deleted(cls, **kwargs):
		filter_query = kwargs.get('filter_query', dict())
		filter_query.update({
			'is_deleted': True
		})
		kwargs.update({
			'filter_query': filter_query
		})
		return cls.count(**kwargs)

	@classmethod
	def view_deleted_multiple(cls, **kwargs):
		filter_query = kwargs.get('filter_query', dict())
		filter_query.update({
			'is_deleted': True
		})
		kwargs.update({
			'filter_query': filter_query
		})
		return cls.view_multiple(**kwargs)

	@classmethod
	def is_deletable(cls, **kwargs):
		
		try:
			instance = kwargs.get('instance')
			# Do something
			return {'success': True, 'message': 'This {0} can be deleted'.format(cls.entity_name)}
		except Exception as e:
			print(e)
			return {'success': False, 'message': 'This {0} can not be deleted'.format(cls.entity_name)}
	
	@classmethod
	def delete(cls,**kwargs):
		try:
			print(kwargs)
			requestor = kwargs.get('requestor')
			instance_id = kwargs.get('instance_id')

			if not cls.entity.objects.filter(id=instance_id).exists():
				return {'success': False, 'message': 'We could not find the {0} you are trying to delete'.format(cls.entity_name)}

			instance = cls.entity.objects.get(id=instance_id)

			validation_data = cls.is_deletable(**{'instance': instance})
			if not validation_data.get('success'):
				return validation_data

			instance.is_deleted = True
			instance.deleted_on = timezone.now()
			instance.deleted_by = requestor
			instance.save()
			return {'success': True, 'message': '{0} deleted successfully'.format(cls.entity_name)}
			
		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not delete the {0}'.format(cls.entity_name)}