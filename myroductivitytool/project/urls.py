from django.conf.urls import url
import myroductivitytool.project.views as project_views

app_name = 'project'

urlpatterns = [
	url(r'^statistics/$', project_views.Statistics.as_view(), name='statistics'),
	url(r'^projects/(?P<pid>\d+)/(?P<action>[-\w]+)/$',
		project_views.Projects.as_view(),
		name='projects'),

	url(r'^projects/(?P<action>[-\w]+)/$',
		project_views.Projects.as_view(),
		name='projects'),
	

	url(r'^tasks/(?P<tid>\d+)/(?P<action>[-\w]+)/$',
		project_views.Tasks.as_view(),
		name='tasks'),

	url(r'^tasks/(?P<action>[-\w]+)/$',
		project_views.Tasks.as_view(),
		name='tasks'),

	url(r'^projects/(?P<pid>\d+)/tasks/(?P<tid>\d+)/(?P<action>[-\w]+)/$',
		project_views.Tasks.as_view(),
		name='tasks'),

	url(r'^projects/(?P<pid>\d+)/tasks/(?P<action>[-\w]+)/$',
		project_views.Tasks.as_view(),
		name='tasks'),


	url(r'^comments/(?P<tcid>\d+)/(?P<action>[-\w]+)/$',
		project_views.TaskComments.as_view(),
		name='comments'),

	url(r'^comments/(?P<action>[-\w]+)/$',
		project_views.TaskComments.as_view(),
		name='comments'),

	url(r'^tasks/(?P<tid>\d+)/comments/(?P<tcid>\d+)/(?P<action>[-\w]+)/$',
		project_views.TaskComments.as_view(),
		name='comments'),

	url(r'^tasks/(?P<tid>\d+)/comments/(?P<action>[-\w]+)/$',
		project_views.TaskComments.as_view(),
		name='comments')
]