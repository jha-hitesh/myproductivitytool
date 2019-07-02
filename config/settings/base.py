
import os
import environ
import datetime
from django.utils.crypto import get_random_string

ROOT_DIR = environ.Path(__file__) - 3  # (myroductivitytool/config/settings/base.py - 3 = myroductivitytool/)
BASE_DIR = str(ROOT_DIR)
APPS_DIR = ROOT_DIR.path('myroductivitytool')

# Load operating system environment variables and then prepare to use them
env = environ.Env()

DEBUG = env.bool('DJANGO_DEBUG', True)

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+,-./:;<=>?@[]^_`{|}~'
SECRET_KEY = get_random_string(50, chars)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    # Third party apps
    'rest_framework',            # utilities for rest apis
    'rest_framework.authtoken',  # token authentication
    'corsheaders',

    # Your apps
    'myroductivitytool.common',
    'myroductivitytool.project'
)

MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myroductivitytool',
        'USER': 'testuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
        'ATOMIC_REQUESTS': True
    }
}

ALLOWED_HOSTS = ["*"]
ROOT_URLCONF = 'config.urls'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
WSGI_APPLICATION = 'config.wsgi.application'


#Migration Modules
MIGRATION_MODULES = {
    'sites': 'myroductivitytool.contrib.sites.migrations'
}

# Static files (CSS, JavaScript, Images)
# ---------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_URL = '/media/'

# Templates
# ----------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates'))
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

# Logging
# ----------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['console'],
        #     'propagate': True,
        # },
        # 'django.server': {
        #     'handlers': ['django.server'],
        #     'level': 'INFO',
        #     'propagate': False,
        # },
        # 'django.request': {
        #     'handlers': ['mail_admins', 'console'],
        #     'level': 'ERROR',
        #     'propagate': False,
        # },
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'INFO'
        # },
    }
}


# Cors Configiration
# ----------------------------------------------------------------
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

CORS_ALLOW_HEADERS = (
    'x-dts-schema',
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://myroductivitytooldemo.herokuapp.com',
    'https://myroductivitytool1000.herokuapp.com'
)

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

# Django Rest Framework
# ----------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', 10)),
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
    'DATE_FORMAT': '%Y-%m-%d',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    )
}

JWT_AUTH = { 
    'JWT_AUTH_COOKIE': 'JWT',
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30)
}


#--------------Additional Configuration-----------------

#Default Settings
EXCEPTION_MESSAGE = 'Exception message'
BAD_REQUEST_MESSAGE = 'We are unable to understand your request.'
NOT_FOUND_MESSAGE = 'We cannot seem to find the page you are looking for'
FORBIDDEN_MESSAGE = 'It seems like you do not have the permission to access this page.'
ENTITY_TOO_LARGE_MESSAGE = 'Request entity too large. Please verify the request contents.'
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
ADMIN_URL = r'^admin/'
