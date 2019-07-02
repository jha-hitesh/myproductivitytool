from django.contrib import admin
from myroductivitytool.project.models import *
from django.apps import apps

for model in apps.get_app_config('project').models.values():
    admin.site.register(model)