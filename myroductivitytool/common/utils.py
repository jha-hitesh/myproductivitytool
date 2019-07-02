import base64
import time
import requests
import json
import re
import pytz
import pprint

from datetime import datetime
from django.utils import timezone
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs
from django.conf import settings
from django.core.paginator import Paginator
from django.utils.crypto import get_random_string

from myroductivitytool.common.models import *


class CommonUtils(object):

	@staticmethod
	def pprint(data, indent=4):
		pp = pprint.PrettyPrinter(indent=indent)
		pp.pprint(data)

	@staticmethod
	def get_time_data_from_seconds(total_seconds):

		try:
			seconds = total_seconds%60
			total_minutes = int(total_seconds/60)
			minutes = total_minutes%60
			total_hours = int(total_minutes/60)
			hours = total_hours%24
			days = int(total_hours/24)

			return {
				'seconds': seconds,
				'minutes': minutes,
				'hours': hours,
				'days': days
			}
		except Exception as e:
			print(e)
			return None

	@staticmethod
	def validate_float_with_precision(number, precison):

		try:
			number = str(number)
			number_split = number.split('.')
			if len(number_split) > 1 and len(number_split[1]) > precison:
				return {'success': False}
			number = float(number)
			if number <= 0:
				return {'success': False}
			return {'success': True, 'number': number}
		except Exception as e:
			print(e)
			return {'success': False}