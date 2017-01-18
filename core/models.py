from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

# Create your models here.

class Action(models.Model):
	user = models.ForeignKey('auth.User')
	action = models.CharField(max_length=140)
	time = models.DateTimeField(default=timezone.now)
	online = models.BooleanField(default=True)

	def update(self, action):
		self.time = timezone.now()
		self.action = action
		self.online = True
		self.save()

	def update_time(self):
		self.time = timezone.now()
		self.online = True
		self.save()

	def offline(self):
		self.online = False
		self.save()

	def __str__(self):
		return self.user.username