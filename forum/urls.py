from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.forum_index, name='forum_index'),
	url(r'^category/(?P<category>\w+)/$', views.category, name='category'),
	url(r'^view/post/(?P<pk>[0-9]+)/$', views.view_post, name='view_post'),
	url(r'^edit/post/(?P<pk>[0-9]+)/$', views.edit_post_page, name='edit_post_page'),
	url(r'^edit/post/(?P<pk>[0-9]+)/submit/$', views.edit_post, name='edit_post'),
	url(r'^reply/post/(?P<pk>[0-9]+)/submit/$', views.reply, name='reply'),
	url(r'^edit/reply/(?P<pk>[0-9]+)/submit/$', views.edit_reply, name='edit_reply'),
	url(r'^lock/post/(?P<pk>[0-9]+)/submit/$', views.lock, name='lock'),
	url(r'^unlock/post/(?P<pk>[0-9]+)/submit/$', views.unlock, name='unlock'),
	url(r'^sticky/post/(?P<pk>[0-9]+)/submit/$', views.sticky, name='sticky'),
	url(r'^unsticky/post/(?P<pk>[0-9]+)/submit/$', views.unsticky, name='unsticky'),
	url(r'^delete/post/(?P<pk>[0-9]+)/submit/$', views.delete, name='delete'),
	url(r'^delete/reply/(?P<pk>[0-9]+)/submit/$', views.delete_reply, name='delete_reply'),
	url(r'^delete/true/reply/(?P<pk>[0-9]+)/submit/$', views.delete_reply_true, name='delete_reply_true'),
	url(r'^(?P<category>\w+)/new/$', views.new_post_page, name='new_post_page'),
	url(r'^new/submit/$', views.new_post, name='new_post'),
	url(r'^bookmarks/$', views.view_bookmarks, name='view_bookmarks'),
	url(r'^view/post/(?P<pk>[0-9]+)/bookmark/$', views.bookmark, name='bookmark'),
	url(r'^bookmarks/delete/(?P<pk>[0-9]+)/$', views.delete_bookmark, name='delete_bookmark'),
]