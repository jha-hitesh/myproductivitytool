import uuid

from django.db import models
from itertools import chain
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField, ArrayField

from myproductivitytool.common.models import *
from myproductivitytool.common.customfields import *


class BaseProjectEntity(models.Model):

	class Meta:
		abstract = True

	name 				= models.CharField(max_length=50)
	description 		= models.TextField()
	start_date 			= models.DateField()
	end_date 			= models.DateField()



class Project(BaseProjectEntity, BaseModel):

	STATUS_CHOICES = (
		('UPC', 'Upcoming'),
		('ONG', 'Ongoing'),
		('CMP', 'Completed')
	)

	status 				= models.CharField(choices=STATUS_CHOICES ,max_length=3)



class Task(BaseProjectEntity, BaseModel):

	STATUS_CHOICES = (
		('DRF', 'Draft'),
		('PRG', 'In Progress'),
		('CMP', 'Completed')
	)

	PRIORITY_CHOICES = (
		('A', 'Low'),
		('B', 'Medium'),
		('C', 'High')
	)

	task_number 		= models.PositiveIntegerField()
	project 			= models.ForeignKey(Project, null=True, blank=True, on_delete=models.DO_NOTHING)
	status 				= models.CharField(choices=STATUS_CHOICES ,max_length=3)
	priority  			= models.CharField(choices=PRIORITY_CHOICES, max_length=2, default='A')



class TaskComment(BaseModel):

	task 				= models.ForeignKey(Task, on_delete=models.DO_NOTHING)
	text 				= models.TextField()



class TaskCommentAttachment(models.Model):

	ATTACHMENT_TYPE_CHOICES = (
		('IMG', 'Image'),
		('PDF', 'Pdf')
	)

	task_comment 		= models.ForeignKey(TaskComment, on_delete=models.DO_NOTHING)
	attachment 			= models.FileField()
	attachment_type 	= models.CharField(choices=ATTACHMENT_TYPE_CHOICES, max_length=3)
