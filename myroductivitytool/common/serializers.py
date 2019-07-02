import serpy
import myroductivitytool.common.serpy_fields as serpy_fields

from myroductivitytool.common.models import *

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

# Common

class ModelIdentitySerializer(serpy.Serializer):

    id          = serpy.IntField(label='id')
    uuid        = serpy_fields.UUIDField(label='uuid', required=False)



class UserSerializer(serpy.Serializer):

    id          = serpy.IntField(label='id')
    username    = serpy.StrField(label='userName')



class BaseModelSerializer(serpy.Serializer):

    id      = serpy.IntField(label='id')
    created_by = UserSerializer(label='createdBy')
    created_on = serpy_fields.DateTimeField(label='createdOn')
    last_modified_by = UserSerializer(label='lastModifiedBy')
    last_modified_on = serpy_fields.DateTimeField(label='lastModifiedOn')
    deleted_by = UserSerializer(label='deletedBy', required=False)
    deleted_on = serpy_fields.DateTimeField(label='deletedOn', required=False)
    is_deleted = serpy.BoolField(label='isDeleted')

    created_by_id = serpy.MethodField('get_created_by_id', label='createdById')
    last_modified_by_id = serpy.MethodField('get_last_modified_by_id', label='lastModifiedById')
    deleted_by_id = serpy.MethodField('get_deleted_by_id', label='deletedById', required=False)

    def get_created_by_id(self, instance):
        return getattr(instance, 'created_by_id')

    def get_last_modified_by_id(self, instance):
        return getattr(instance, 'last_modified_by_id')

    def get_deleted_by_id(self, instance):
        return getattr(instance, 'deleted_by_id')