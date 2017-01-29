from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

class Category(models.Model):
	overarching_category = models.CharField(max_length=56)
	name = models.CharField(max_length=56)
	description = models.CharField(max_length=140)

	def __str__(self):
		return self.name

class Post(models.Model):
	author = models.ForeignKey('auth.User')
	post_time = models.DateTimeField(default=timezone.now)

	category = models.ForeignKey(Category)

	title = models.CharField(max_length=140, null=True, blank=True)
	body_text = models.TextField(null=True, blank=True)

	locked   = models.BooleanField(default=False)
	stickied = models.BooleanField(default=False)
	deleted  = models.BooleanField(default=False)

	important = models.BooleanField(default=False)

	def __str__(self):
		return self.title

class Reply(models.Model):
	author = models.ForeignKey('auth.User')
	post_time = models.DateTimeField(default=timezone.now)
	original = models.ForeignKey(Post)

	body_text = models.TextField()

	deleted = models.BooleanField(default=False)
	deleted_reason = models.CharField(max_length=140, default="", null=True, blank=True)

	def __str__(self):
		return self.body_text

class Bookmark(models.Model):
	bookmarker = models.ForeignKey('auth.user')
	post = models.ForeignKey(Post)
	last_viewed = models.DateTimeField(default=timezone.now, null=True, blank=True)

	def __str__(self):
		return self.post.title





