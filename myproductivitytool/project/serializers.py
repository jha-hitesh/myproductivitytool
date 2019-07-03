import serpy
import myproductivitytool.common.serpy_fields as serpy_fields

from myproductivitytool.project.models import *
from myproductivitytool.common.serializers import *

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static


# Project

class BaseProjectEntitySerializer(serpy.Serializer):

    name            = serpy.StrField(label='name')
    description     = serpy.StrField(label='description')
    start_date      = serpy_fields.DateField(label='startDate')
    end_date        = serpy_fields.DateField(label='endDate')
    status          = serpy.StrField(label='status')
    duration        = serpy.MethodField('get_duration', label='duration')

    def get_duration(self, instance):
        return ''



class ProjectSerializer(BaseProjectEntitySerializer, BaseModelSerializer):

    pass


class TaskSerializer(BaseProjectEntitySerializer, BaseModelSerializer):

    project     = ProjectSerializer(label='project', required=False)
    project_id  = serpy.MethodField('get_project_id' ,label='projectId', required=False)
    priority    = serpy.StrField(label='priority')
    priority_full = serpy.MethodField('get_priority_full', label='priorityFull')

    def get_priority_full(self, instance):
        return instance.get_priority_display()

    def get_project_id(self, instance):
        return getattr(instance, 'project_id')



class TaskCommentSerializer(BaseModelSerializer):

    task        = TaskSerializer(label='task')
    text        = serpy.StrField(label='text')


class TaskCommentAttachmentSerializer(BaseModelSerializer):

    task_comment = TaskCommentSerializer(label='taskComment')
    attachment   =  serpy.MethodField('get_attachment_url', label='attachment')
    attachment_type = serpy.StrField(label='attachmentType')

    def get_attachment_url(self, instance):
        try:
            return '{0}{1}'.format(settings.BACKEND_URL, instance.attachment.url)
        except Exception as e:
            print(e)