import serpy
from datetime import datetime
from django.conf import settings

class DateField(serpy.Field):
	def to_value(self, value):
		if value:
			return value.strftime(settings.DATE_FORMAT)


class DateTimeField(serpy.Field):
	def to_value(self, value):
		if value:
			return value.strftime(settings.DATETIME_FORMAT)


class UUIDField(serpy.Field):
	def to_value(self, value):
		if value:
			return value.hex


class JSONField(serpy.Field):
	def to_value(self, value):
		if value:
			return value


class FileField(serpy.Field):
	def to_value(self, value):
		if value:
			return value.url
