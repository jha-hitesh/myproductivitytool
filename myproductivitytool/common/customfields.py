import json

from hashlib import sha256
from django.forms import forms
from django.conf import settings
from django.utils import timezone
from django.db.models import FileField
from django.db import models, connection
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat


def upload_to(inst, fname):
	f = sha256((fname + str(timezone.now())).encode('utf-8')).hexdigest()
	f += fname

	path = '/'.join([inst.__class__.__name__, f])

	print('Path for upload, for {0} --> {1}'.format(inst.__class__.__name__, path))
	
	return path



class ContentTypeRestrictedFileField(FileField):
	"""
	Same as FileField, but you can specify:
		* content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
		* max_upload_size - a number indicating the maximum file size allowed for upload.
			2.5MB - 2621440
			5MB - 5242880
			10MB - 10485760
			20MB - 20971520
			50MB - 52428800
			100MB 104857600
			250MB - 214958080
			500MB - 429916160
	"""
	def __init__(self, *args, **kwargs):
		self.max_upload_size = kwargs.pop("max_upload_size", 52428800)
		super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

		file = data.file
		try:
			if file._size > self.max_upload_size:
				raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
		except AttributeError:
			pass

		return data
