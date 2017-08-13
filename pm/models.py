from __future__ import unicode_literals
from django.utils import timezone
from django.db import models

# Create your models here.
class PM(models.Model):
	sending_user = models.ForeignKey('auth.User', related_name="pm_sending_user")
	receiving_user = models.ForeignKey('auth.User', related_name="pm_receiving_user")

	subject = models.CharField(max_length=140, blank=True, null=True)
	message = models.TextField(blank=True, null=True)

	send_time = models.DateTimeField(default=timezone.now)
	seen = models.BooleanField(default=False)

	replied = models.BooleanField(default=False)
	removed_by_sender = models.BooleanField(default=False)
	removed_by_receiver = models.BooleanField(default=False)

	parent_pm = models.ForeignKey('self', blank=True, null=True)

	def __str__(self):
		if self.parent_pm is not None:
			name = self.sending_user.username + "'s reply to " + self.receiving_user.username
		else:
			name = self.sending_user.username + "'s message to " + self.receiving_user.username
		return name