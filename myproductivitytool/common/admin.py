from django.contrib import admin
from myproductivitytool.common.models import *
from django.apps import apps

for model in apps.get_app_config('common').models.values():
    admin.site.register(model)