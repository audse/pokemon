from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

	# STATIC PAGES
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login_page, name='login_page'),
	url(r'^register/$', views.register_page, name='register_page'),
	url(r'^user/(?P<username>\w+)/$', views.profile_page, name='profile_page'),
	url(r'^users/online/$', views.online_page, name='online_page'),

	# FUNCTION PAGES
	url(r'^login/auth/$', views.login, name='login'),
	url(r'^logout/auth/$', views.logout, name='logout'),
	url(r'^register/auth/$', views.register, name='register'),

	# ERROR PAGES
	url(r'^error/auth/none/$', views.must_be_logged_in, name='must_be_logged_in'),
	url(r'^error/auth/toomuch/$', views.cannot_be_logged_in, name='cannot_be_logged_in'),
	url(r'^error/user/none/$', views.user_not_found, name='user_not_found'),
	url(r'^login/failed/$', views.login_failed, name='login_failed'),
	url(r'^error/interaction/$', views.cannot_interact, name='cannot_interact'),
	url(r'^error/auth/$', views.cannot_access, name='cannot_access'),

	# SITE FUNCTIONS PAGES
	url(r'^lab/$', views.lab, name='lab'),
	url(r'^lab/reload/$', views.lab_reload, name='lab_reload'),
	url(r'^lab/adopt/(?P<pk>[0-9]+)/$', views.lab_adopt, name='lab_adopt'),
	url(r'^(?P<username>\w+)/interact/(?P<pk>[0-9]+)/$', views.interact, name='interact'),
	url(r'^pokemon/view/(?P<pk>[0-9]+)/$', views.view_adopt, name='view_adopt'),
	url(r'^egg/hatch/(?P<pk>[0-9]+)/$', views.hatch_egg, name='hatch_egg'),
	url(r'^boxes/$', views.boxes, name='boxes'),
	url(r'^boxes/create/$', views.create_box_page, name='create_box_page'),
	url(r'^boxes/create/processsing/$', views.create_box, name='create_box'),
]