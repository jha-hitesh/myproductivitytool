import uuid
import json

from django.db import models
from itertools import chain
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from myroductivitytool.common.customfields import *


class BaseModel(models.Model):

	class Meta:
		abstract = True
	
	created_by 		= models.ForeignKey(User, 
							related_name='%(app_label)s_%(class)s_creator', on_delete=models.DO_NOTHING)
	created_on 		= models.DateTimeField(auto_now_add=True)
	last_modified_by 	= models.ForeignKey(User, 
							related_name='%(app_label)s_%(class)s_modifier', on_delete=models.DO_NOTHING)
	last_modified_on		= models.DateTimeField(auto_now=True)
	deleted_by		= models.ForeignKey(User, null=True, blank=True, 
							related_name='%(app_label)s_%(class)s_deleter', on_delete=models.DO_NOTHING)
	deleted_on		= models.DateTimeField(null=True, blank=True)
	is_deleted		= models.BooleanField(default=False)
	
	def save(self, *args, **kwargs):
	
		if not self.id or not self.created_on:
			self.created_on = timezone.now()
	
		return super(BaseModel,	self).save(*args, **kwargs)