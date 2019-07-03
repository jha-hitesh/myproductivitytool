from .base import *
import os
import environ
import dj_database_url
import django_heroku

# keeping srcret key static for server
SECRET_KEY = 'P]URJ(&=-vH^6i(p|jyW;r_<(EHkB[g-hQT3K[-jL[KD;u2D5:'
env = environ.Env()
DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'])}

django_heroku.settings(locals())

DEBUG = False
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    # Third party apps
    'rest_framework',            # utilities for rest apis
    'rest_framework.authtoken',  # token authentication
    'corsheaders',
    'storages',

    # Your apps
    'myproductivitytool.common',
    'myproductivitytool.project'
)

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DROPBOX_OAUTH2_TOKEN = os.environ['dropbox_token']

BACKEND_URL = 'https://myproductivitytool.herokuapp.com'
FRONTEND_URL = 'https://myproductivitytoolui.herokuapp.com'