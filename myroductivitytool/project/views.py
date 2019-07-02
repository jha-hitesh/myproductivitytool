from myroductivitytool.common.utils import *
from myroductivitytool.common.models import * 
from myroductivitytool.common.responses import *
from myroductivitytool.common.serializers import *
from myroductivitytool.common.services import *

from myroductivitytool.project.utils import *
from myroductivitytool.project.models import * 
from myroductivitytool.project.serializers import *
from myroductivitytool.project.services import *

from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import authentication
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View, FormView, TemplateView


class Statistics(APIView):

	def get(self, request, *args, **kwargs):

		try:
			statistics_data = {
				'projects': ProjectService.count_active(**{'filter_query':{'created_by': request.user}}).get('count'),
				'tasks': TaskService.count_active(**{'filter_query':{'created_by': request.user}}).get('count'),
			}

			return success(statistics_data)

		except Exception as e:
			print(e)
			return exception(message='We could not load Statistics for the dashboard')



class Projects(APIView):

	SERVICE_OWNER = ProjectService

	def get(self, request, pid=None, action=None, *args, **kwargs):

		try:
			employee = request.user
			data = request.GET.dict()

			if action not in self.SERVICE_OWNER.ALLOWED_ACTIONS_FOR_GET:
				return bad_request(message='The requested action is not available on given resource')

			if action == 'get_context':
				service_keywords = dict()
				if pid:
					service_keywords.update({'instance_id': pid})

			else:
				service_response = self.SERVICE_OWNER.construct_filter_query(**data)
				if not service_response.get('success'):
					return exception(message=service_response.get('message'))

				filter_query = service_response.get('filter_query')

				service_response = self.SERVICE_OWNER.construct_page_query(**data)
				if not service_response.get('success'):
					return exception(message=service_response.get('message'))

				page_query = service_response.get('page_query')

				if pid:
					filter_query.update({'id': pid})

				# to make sure only user created data is sent
				filter_query.update({
					'created_by': request.user
				})

				service_keywords = {
					'page_query': page_query,
					'filter_query': filter_query
				}

			service_response = getattr(self.SERVICE_OWNER, action)(**service_keywords)
			if not service_response.get('success'):
				return exception(message=service_response.get('message'))
			return Response(service_response)

		except Exception as e:
			print(e)
			return exception(message='We could not perform the requested action on the given resource')


	def post(self, request, pid=None, action=None, *args, **kwargs):

		try:
			employee = request.user
			data = request.POST.dict()
			if action not in self.SERVICE_OWNER.ALLOWED_ACTIONS_FOR_POST:
				return bad_request(message='The requested action is not available on given resource')

			# For delete Action
			if action in ['delete']:
				service_response = getattr(self.SERVICE_OWNER, action)(**{
					'instance_id': pid
				})
				message = service_response.get('message')
				if service_response.get('success'):
					return success(service_response)
				else:
					return exception(message=message)

			# For Add Update Action

			if action == 'update' and not pid:
				return bad_request(message='We could not find the project for updation')

			if action == 'add':
				pid = None

			entity_data = dict()
			# Validate always mendatory fields

			mandatory_fields = [
				('name', 'Please provide a name'),
				('startDate', 'Please provide a start date'),
				('endDate', 'Please provide a end date'),
				('description', 'Please provide a description'),
				('status', 'Please provide a status for this project'),
			]

			for field in mandatory_fields:
				value = data.get(field[0], None)
				if not value or not len(value.strip()):
					return bad_request(message=field[1])

			start_date = datetime.strptime(data.get('startDate'), settings.DATE_FORMAT)
			end_date = datetime.strptime(data.get('endDate'), settings.DATE_FORMAT)

			if start_date > end_date:
				return exception(message='Start date can not be greater than end date')

			avatar = request.FILES.get('avatar', None)
			keep_previous_avatar = data.get('keepPreviousAvatar', 'no')

			status = data.get('status')
			if status not in ['UPC', 'ONG', 'CMP']:
				return bad_request(message='The status selected is invalid')

			# Fetch always mendatory fields

			entity_data.update({
				'avatar': avatar,
				'status': status,
				'end_date': end_date,
				'name': data.pop('name'),
				'start_date': start_date,
				'last_modified_by': employee,			
				'description': data.pop('description')
			})

			overlapping_projects = Project.objects.filter(name=entity_data.get('name'), is_deleted=False)
			if pid:
				if overlapping_projects.exclude(id=pid).exists():
					return exception(message='A project with same name already exists')

				instance = Project.objects.get(id=pid)
				if keep_previous_avatar == 'yes':
					entity_data.update({'avatar': instance.avatar})

				for field_name, field_value in entity_data.items():
					setattr(instance, field_name, field_value)
				instance.save()
				final_message = 'Project updated successfully'
			else:
				if overlapping_projects.exists():
					return exception(message='A project with same name already exists')
				entity_data.update({'created_by': employee})
				instance = Project.objects.create(**entity_data)
				final_message = 'Project created successfully'

			response_json = {
				'message': final_message
			}
			return success(response_json)

		except Exception as e:
			print(e)
			return exception(message='We could not perform the requested action on the given resource')



class Tasks(APIView):

	SERVICE_OWNER = TaskService

	def get(self, request, pid=None, tid=None, action=None, *args, **kwargs):

		try:
			employee = request.user
			data = request.GET.dict()

			if action not in self.SERVICE_OWNER.ALLOWED_ACTIONS_FOR_GET:
				return bad_request(message='The requested action is not available on given resource')

			if action == 'get_context':
				service_keywords = dict()
				if tid:
					service_keywords.update({'instance_id': tid})

			else:
				service_response = self.SERVICE_OWNER.construct_filter_query(**data)
				if not service_response.get('success'):
					return exception(message=service_response.get('message'))

				filter_query = service_response.get('filter_query')

				service_response = self.SERVICE_OWNER.construct_page_query(**data)
				if not service_response.get('success'):
					return exception(message=service_response.get('message'))

				page_query = service_response.get('page_query')

				if tid:
					filter_query.update({'id': tid})
				if pid:
					filter_query.update({'project__id': pid})

				# to make sure only user created data is sent
				filter_query.update({
					'created_by': request.user
				})

				service_keywords = {
					'page_query': page_query,
					'filter_query': filter_query
				}

			service_response = getattr(self.SERVICE_OWNER, action)(**service_keywords)
			if not service_response.get('success'):
				return exception(message=service_response.get('message'))
			return Response(service_response)

		except Exception as e:
			print(e)
			return exception(message='We could not perform the requested action on the given resource')


	def post(self, request, pid=None, tid=None, action=None, *args, **kwargs):

		try:
			employee = request.user
			data = request.POST.dict()
			if action not in self.SERVICE_OWNER.ALLOWED_ACTIONS_FOR_POST:
				return bad_request(message='The requested action is not available on given resource')

			# For delete Action
			if action in ['delete']:
				service_response = getattr(self.SERVICE_OWNER, action)(**{
					'instance_id': tid
				})
				message = service_response.get('message')
				if service_response.get('success'):
					return success(service_response)
				else:
					return exception(message=message)

			# For Add Update Action

			if action == 'update' and not tid:
				return bad_request(message='We could not find the task for updation')

			if action == 'add':
				tid = None

			entity_data = dict()
			# Validate always mendatory fields

			mandatory_fields = [
				('name', 'Please provide a name'),
				('startDate', 'Please provide a start date'),
				('endDate', 'Please provide a end date'),
				('description', 'Please provide a description'),
				('status', 'Please provide a status'),
				('priority', 'Please provide a priority')
			]

			for field in mandatory_fields:
				value = data.get(field[0], None)
				if not value or not len(value.strip()):
					return bad_request(message=field[1])

			start_date = datetime.strptime(data.get('startDate'), settings.DATE_FORMAT)
			end_date = datetime.strptime(data.get('endDate'), settings.DATE_FORMAT)

			if start_date > end_date:
				return exception(message='Start date can not be greater than end date')

			project = None
			if data.get('project', None):
				project = Project.objects.get(id=data.get('project'))

			status = data.pop('status')
			if status not in ['DRF', 'PRG', 'CMP']:
				return bad_request(message='The status provided is invalid')

			priority = data.pop('priority')
			if priority not in ['A', 'B', 'C']:
				return bad_request(message='The priority provided is invalid')

			# Fetch always mendatory fields

			entity_data.update({
				'status': status,			
				'project': project,
				'priority': priority,
				'end_date': end_date,
				'name': data.pop('name'),
				'start_date': start_date,
				'last_modified_by': employee,
				'description': data.pop('description')
			})
			overlapping_tasks = Task.objects.filter(name=entity_data.get('name'), is_deleted=False)
			if project:
				overlapping_tasks = overlapping_tasks.filter(project=project)
			else:
				overlapping_tasks = overlapping_tasks.filter(project__isnull=True)
			if tid:
				if overlapping_tasks.exclude(id=tid).exists():
					return exception(message='A task with same name already exists{0}'.format(' under the selected project' if project else ''))

				instance = Task.objects.get(id=tid)
				for field_name, field_value in entity_data.items():
					setattr(instance, field_name, field_value)
				instance.save()
				final_message = 'Task updated successfully'
			else:
				if overlapping_tasks.exists():
					return exception(message='A task with same name already exists{0}'.format(' under the selected project' if project else ''))

				service_response = self.SERVICE_OWNER.generate_task_number()
				if not service_response.get('success'):
					return exception(message=service_response.get('message'))

				entity_data.update({
					'created_by': employee,
					'task_number': service_response.get('task_number')
				})
				instance = Task.objects.create(**entity_data)
				final_message = 'Task created successfully'
				
			response_json = {
				'message': final_message
			}
			return success(response_json)

		except Exception as e:
			print(e)
			return exception(message='We could not perform the requested action on the given resource')



class TaskComments(APIView):

	SERVICE_OWNER = TaskCommentService

	def get(self, request, tid=None, tcid=None, action=None, *args, **kwargs):

		try:
			employee = request.user
			data = request.GET.dict()

			if action not in self.SERVICE_OWNER.ALLOWED_ACTIONS_FOR_GET:
				return bad_request(message='The requested action is not available on given resource')

			if action == 'get_context':
				service_keywords = dict()
				if tcid:
					service_keywords.update({'instance_id': tcid})

			else:
				service_response = self.SERVICE_OWNER.construct_filter_query(**data)
				if not service_response.get('success'):
					return exception(message=service_response.get('message'))

				filter_query = service_response.get('filter_query')

				service_response = self.SERVICE_OWNER.construct_page_query(**data)
				if not service_response.get('success'):
					return exception(message=service_response.get('message'))

				page_query = service_response.get('page_query')

				if tcid:
					filter_query.update({'id': tcid})
				if tid:
					filter_query.update({'task__id': tid})

				# to make sure only user created data is sent
				filter_query.update({
					'created_by': request.user
				})

				service_keywords = {
					'page_query': page_query,
					'filter_query': filter_query
				}

			service_response = getattr(self.SERVICE_OWNER, action)(**service_keywords)
			if not service_response.get('success'):
				return exception(message=service_response.get('message'))
			return Response(service_response)

		except Exception as e:
			print(e)
			return exception(message='We could not perform the requested action on the given resource')


	def post(self, request, tid=None, tcid=None, action=None, *args, **kwargs):

		try:
			employee = request.user
			data = request.POST.dict()
			if action not in self.SERVICE_OWNER.ALLOWED_ACTIONS_FOR_POST:
				return bad_request(message='The requested action is not available on given resource')

			# For delete Action
			if action in ['delete']:
				service_response = getattr(self.SERVICE_OWNER, action)(**{
					'instance_id': tcid
				})
				message = service_response.get('message')
				if service_response.get('success'):
					return success(service_response)
				else:
					return exception(message=message)

			# For Add Update Action

			if action == 'update' and not tcid:
				return bad_request(message='We could not find the task comment for updation')

			if action == 'add':
				tcid = None

			entity_data = dict()
			# Validate always mendatory fields

			mandatory_fields = [
				('text', 'Please provide a comment text'),
				('task', 'Please provide a task against you are adding comment')
			]

			for field in mandatory_fields:
				value = data.get(field[0], None)
				if not value or not len(value.strip()):
					return bad_request(message=field[1])

			task = Task.objects.get(id=data.get('task'))
			text = data.get('text').strip()

			# Fetch always mendatory fields

			entity_data.update({
				'text': text,			
				'task': task,
				'last_modified_by': employee
			})
			
			if tcid:
				instance = TaskComment.objects.get(id=tcid)
				for field_name, field_value in entity_data.items():
					setattr(instance, field_name, field_value)
				instance.save()
				final_message = 'Task comment updated successfully'
			else:
				entity_data.update({
					'created_by': employee,
				})
				instance = TaskComment.objects.create(**entity_data)
				final_message = 'Task comment added successfully'
				
			response_json = {
				'message': final_message
			}
			return success(response_json)

		except Exception as e:
			print(e)
			return exception(message='We could not perform the requested action on the given resource')



class TaskCommentAttachment(APIView):

	SERVICE_OWNER = TaskCommentAttachmentService

	def get(self, request, tcid=None, tcaid=None, action=None, *args, **kwargs):

		try:
			employee = request.user
			data = request.GET.dict()

			if action not in self.SERVICE_OWNER.ALLOWED_ACTIONS_FOR_GET:
				return bad_request(message='The requested action is not available on given resource')

			if action == 'get_context':
				service_keywords = dict()
				if tcaid:
					service_keywords.update({'instance_id': tcaid})

			else:
				service_response = self.SERVICE_OWNER.construct_filter_query(**data)
				if not service_response.get('success'):
					return exception(message=service_response.get('message'))

				filter_query = service_response.get('filter_query')

				service_response = self.SERVICE_OWNER.construct_page_query(**data)
				if not service_response.get('success'):
					return exception(message=service_response.get('message'))

				page_query = service_response.get('page_query')

				if tcaid:
					filter_query.update({'id': tcaid})
				if tcid:
					filter_query.update({'task_comment__id': tcid})

				# to make sure only user created data is sent
				filter_query.update({
					'created_by': request.user
				})

				service_keywords = {
					'page_query': page_query,
					'filter_query': filter_query
				}

			service_response = getattr(self.SERVICE_OWNER, action)(**service_keywords)
			if not service_response.get('success'):
				return exception(message=service_response.get('message'))
			return Response(service_response)

		except Exception as e:
			print(e)
			return exception(message='We could not perform the requested action on the given resource')


	def post(self, request, tcid=None, tcaid=None, action=None, *args, **kwargs):

		try:
			employee = request.user
			data = request.POST.dict()
			if action not in self.SERVICE_OWNER.ALLOWED_ACTIONS_FOR_POST:
				return bad_request(message='The requested action is not available on given resource')

			# For delete Action
			if action in ['delete']:
				service_response = getattr(self.SERVICE_OWNER, action)(**{
					'instance_id': tcaid
				})
				message = service_response.get('message')
				if service_response.get('success'):
					return success(service_response)
				else:
					return exception(message=message)

			# For Add Update Action

			if action == 'update' and not tcaid:
				return bad_request(message='We could not find the task comment attachment for updation')

			if action == 'add':
				tcaid = None

			entity_data = dict()
			# Validate always mendatory fields

			mandatory_fields = [
				('taskComment', 'Please provide a task comment against you are adding attachment')
			]

			for field in mandatory_fields:
				value = data.get(field[0], None)
				if not value or not len(value.strip()):
					return bad_request(message=field[1])

			task_comment = TaskComment.objects.get(id=data.get('taskComment'))
			attachment = request.FILES.get('attachment')

			# Fetch always mendatory fields

			entity_data.update({
				'attachment': attachment,			
				'task_comment': task_comment,
			})
			
			if tcaid:
				instance = Task.objects.get(id=tcaid)
				for field_name, field_value in entity_data.items():
					setattr(instance, field_name, field_value)
				instance.save()
				final_message = 'Task comment attachment updated successfully'
			else:
				service_response = self.SERVICE_OWNER.generate_task_number()
				if not service_response.get('success'):
					return exception(message=service_response.get('message'))

				instance = Task.objects.create(**entity_data)
				final_message = 'Task comment attachment added successfully'
				
			response_json = {
				'message': final_message
			}
			return success(response_json)

		except Exception as e:
			print(e)
			return exception(message='We could not perform the requested action on the given resource')
