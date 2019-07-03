import calendar

from myproductivitytool.common.utils import *
from myproductivitytool.common.models import * 
from myproductivitytool.common.responses import *
from myproductivitytool.common.serializers import *
from myproductivitytool.common.services import *

from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import authentication
from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View, FormView, TemplateView


@method_decorator(csrf_exempt, name='dispatch')
class GetJWTToken(View):

	def post(self, request, *args, **kwargs):

		try:
			username = request.POST.get('username', None)
			password = request.POST.get('password', None)

			if not username or not password:
				return bad_request(message='Please provide both username and password')

			user = User.objects.filter(username=username.strip()).first()
			if not user:
				return exception(message='No user exists for this username')
			
			if not user.check_password(password.strip()):
				return exception(message='Your password is incorrect')

			jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
			jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
			payload = jwt_payload_handler(user)
			payload['orig_iat'] = calendar.timegm(datetime.utcnow().utctimetuple())
			token = jwt_encode_handler(payload)

			return success({'token': token})

		except Exception as e:
			print(e)
			return exception(message='We could not log you in')


class verifyJWTToken(APIView):

	def get(self, request, *args, **kwargs):

		return success({'message': 'Token valid'})

@method_decorator(csrf_exempt, name='dispatch')
class SignUp(View):

	def post(self, request, *args, **kwargs):

		try:
			data = request.POST.dict()

			mandatory_fields = (
				('firstName', 'Please provide your first name'),
				('lastName', 'Please provide your last name'),
				('email', 'Please provide your email address'),
				('username', 'Please provide a username of your choice'),
				('password', 'Please provide a password of your choice')
			)

			first_name = data.get('firstName').strip()
			last_name = data.get('lastName').strip()
			email = data.get('email').strip()
			username = data.get('username').strip()
			password = data.get('password').strip()

			for field_data in mandatory_fields:
				field_value = data.get(field_data[0], None)
				if not field_value or not field_value.strip():
					return bad_request(field_data[1])

			if User.objects.filter(email=email).exists():
				return exception(message='This email has already been used to sign up with us')

			if User.objects.filter(username=username).exists():
				return exception(message='This username has already been taken')

			if len(password) < 8:
				return bad_request(message='Please provide a password with at least 8 characters')

			new_user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
			
			return success({'message': 'You have successfully signed up'})
		except Exception as e:
			print(e)
			return exception(message='We could not sign you up')