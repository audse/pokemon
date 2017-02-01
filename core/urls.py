from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

	# STATIC PAGES
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login_page, name='login_page'),
	url(r'^register/$', views.register_page, name='register_page'),
	url(r'^user/(?P<username>.*)/$', views.profile_page, name='profile_page'),
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
	url(r'^error/auth/staff$', views.staff_only, name='staff_only'),

	# LAB PAGES
	url(r'^lab/$', views.lab, name='lab'),
	url(r'^lab/reload/$', views.lab_reload, name='lab_reload'),
	url(r'^lab/adopt/(?P<pk>[0-9]+)/$', views.lab_adopt, name='lab_adopt'),

	# INTERACTING WITH ADOPTS PAGES
	url(r'^(?P<username>.*)/interact/(?P<pk>[0-9]+)/$', views.interact, name='interact'),
	url(r'^pokemon/view/(?P<pk>[0-9]+)/$', views.view_adopt, name='view_adopt'),
	url(r'^pokemon/view/(?P<pk>[0-9]+)/nickname/$', views.change_nickname, name='change_nickname'),
	url(r'^pokemon/evolve/exp/(?P<pk>[0-9]+)/$', views.evolve_by_level, name='evolve_by_level'),
	url(r'^egg/hatch/(?P<pk>[0-9]+)/$', views.hatch_egg, name='hatch_egg'),

	# BOXES PAGES
	url(r'^boxes/$', views.boxes, name='boxes'),
	url(r'^boxes/create/$', views.create_box_page, name='create_box_page'),
	url(r'^boxes/create/processsing/$', views.create_box, name='create_box'),
	url(r'^boxes/(?P<box>[0-9]+)/move/(?P<adopt>[0-9]+)/$', views.move_to_box, name='move_to_box'),
	url(r'^boxes/position/$', views.update_position, name='update_position'),
	url(r'^update/action/$', views.manually_update_online, name='manually_update_online'),

	# POKEDEX PAGES
	url(r'^dex/$', views.pokedex_index, name='pokedex_index'),
	url(r'^dex/receive/$', views.receive_pokedex, name='receive_pokedex'),

	# PARK PAGES
	url(r'^park/$', views.park, name='park'),
	url(r'^park/adopt/(?P<pk>[0-9]+)/$', views.park_adopt, name='park_adopt'),
	url(r'^pokemon/view/(?P<pk>[0-9]+)/release$', views.release_adopt, name='release_adopt'),

	# WEB SCRAPE
	url(r'^web/scrape/data/$', views.pokemon_web_scrape, name='pokemon_web_scrape'),
]




