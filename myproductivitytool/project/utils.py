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

from myproductivitytool.common.models import *