from myroductivitytool.common.services import *
from myroductivitytool.project.models import *

from myroductivitytool.project.serializers import *

from django.db.models.functions import Concat
from django.db.models import F, Value, CharField


class BaseProjectEntityService(ModelService):

	entity = BaseProjectEntity
	entity_name = 'Base Project Entity'
	entity_serializer = BaseProjectEntitySerializer



class TaskService(BaseModelService):

	entity = Task
	entity_name = 'Project Task'
	entity_serializer = TaskSerializer

	@classmethod
	def get_context(cls, **kwargs):
		try:
			context = dict()
			instance_id = kwargs.get('instance_id', None)
			projects = list(Project.objects.filter(is_deleted=False).annotate(key=F('id'), value=F('id'), text=F('name')).values('key','value', 'text'))
			context.update({
				'projects': projects
			})
			if instance_id:
				instance = cls.entity.objects.get(id=instance_id)
				instance = cls.entity_serializer(instance).data
				context.update({
					'instance': instance
				})
			print(context)
			return {'success': True, 'context': context}
		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not fetch context for {0}'.format(cls.entity_name)}

	@classmethod
	def generate_task_number(cls, **kwargs):

		try:
			return {'success': True, 'task_number':Task.objects.count()+1}
		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not generate task number'}


class ProjectService(BaseModelService):

	entity = Project
	entity_name = 'Project'
	entity_serializer = ProjectSerializer

	@classmethod
	def delete(cls,**kwargs):
		try:
			requestor = kwargs.get('requestor')
			instance_id = kwargs.get('instance_id')

			if not cls.entity.objects.filter(id=instance_id).exists():
				return {'success': False, 'message': 'We could not find the {0} you are trying to delete'.format(cls.entity_name)}

			instance = cls.entity.objects.get(id=instance_id)

			validation_data = cls.is_deletable(**{'instance': instance})
			if not validation_data.get('success'):
				return validation_data

			# remove project from attached tasks
			Task.objects.filter(project=instance).update(project=None)
			
			instance.is_deleted = True
			instance.deleted_on = timezone.now()
			instance.deleted_by = requestor
			instance.save()
			return {'success': True, 'message': '{0} deleted successfully'.format(cls.entity_name)}
			
		except Exception as e:
			print(e)
			return {'success': False, 'message': 'We could not delete the {0}'.format(cls.entity_name)}


class TaskCommentService(BaseModelService):

	entity = TaskComment
	entity_name = 'Task Comment'
	entity_serializer = TaskCommentSerializer


class TaskCommentAttachmentService(BaseModelService):

	entity = TaskCommentAttachment
	entity_name = 'Task Comment Attachment'
	entity_serializer = TaskCommentAttachmentSerializer



