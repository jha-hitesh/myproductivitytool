import json

from django.conf import settings
from django.http import HttpResponse
from django.template.response import TemplateResponse


def success(payload):
	response = HttpResponse(json.dumps(payload), 
		content_type='application/json')
	response.status_code = 200

	return response


def bad_request(**kwargs):

	message = kwargs.get('message', settings.BAD_REQUEST_MESSAGE)
	kwargs.update({'message': message})

	response = HttpResponse(json.dumps(kwargs), 
		content_type='application/json')
	response.status_code = 400

	return response


def forbidden(**kwargs):

	message = kwargs.get('message', settings.FORBIDDEN_MESSAGE)
	kwargs.update({'message': message})
	
	response = HttpResponse(json.dumps(kwargs), 
		content_type='application/json')
	response.status_code = 403

	return response


def not_found(**kwargs):

	message = kwargs.get('message', settings.NOT_FOUND_MESSAGE)
	kwargs.update({'message': message})
	
	response = HttpResponse(json.dumps(kwargs), 
		content_type='application/json')
	response.status_code = 404

	return response

def exception(**kwargs):

	message = kwargs.get('message', settings.EXCEPTION_MESSAGE)
	kwargs.update({'message': message})

	response = HttpResponse(json.dumps(kwargs), 
		content_type='application/json')
	response.status_code = 500

	return response



class ErrorResponse(TemplateResponse):
	
	def __init__(self, request, template, context, status):
		super(ErrorResponse, self).__init__(request, template,
			context, status)