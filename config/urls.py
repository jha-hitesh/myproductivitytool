from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls import handler400, handler403, handler404, handler500


from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # jwt urls
    url(r'^auth-jwt/$', obtain_jwt_token, name='auth-jwt'),
    url(r'^auth-jwt-refresh/$', refresh_jwt_token, name='auth-jwt-refresh'),
    url(r'^auth-jwt-verify/$', verify_jwt_token, name='auth-jwt-verify'),

    # Your stuff: custom urls includes go here

    url(r'^api/', 
        include('myproductivitytool.project.urls', 
            namespace='projects')),

    url(r'^api/common/', 
        include('myproductivitytool.common.urls', 
            namespace='common')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)