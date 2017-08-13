from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^$', views.pm_index, name='pm_index'),
	url(r'^send/(?P<username>.*)/$', views.send_pm_page, name='send_pm_page'),
	url(r'^sending/$', views.send_pm, name='send_pm'),
	url(r'^reply/(?P<pk>[0-9]+)/$', views.reply_page, name='reply_page'),
	url(r'^reply/sending/$', views.reply, name='reply'),
	url(r'^read/(?P<pk>[0-9]+)/$', views.mark_as_read, name='mark_as_read'),
	url(r'^remove/sent/(?P<pk>[0-9]+)/$', views.remove_from_sent, name='remove_from_sent'),
	url(r'^remove/received/(?P<pk>[0-9]+)/$', views.remove_from_received, name='remove_from_received'),
]




