from django.conf.urls import url
import myproductivitytool.common.views as common_views

app_name = 'common'

urlpatterns = [
	url(r'^get-jwt/$', common_views.GetJWTToken.as_view(), name='get-jwt'),
	url(r'^signup/$', common_views.SignUp.as_view(), name='signup'),
	url(r'^verify-jwt/$', common_views.verifyJWTToken.as_view(), name='verify-jwt'),
	]