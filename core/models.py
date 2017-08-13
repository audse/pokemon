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

class Currency(models.Model):
	user = models.ForeignKey('auth.User')
	pd = models.IntegerField(default=500)
	coins = models.IntegerField(default=0)

	def get_pd(self, pd_amount):
		self.pd = self.pd + pd_amount
		self.save()

	def get_coins(self, coins_amount):
		self.coins = self.coins + coins_amount
		self.save()

	def spend_coins(self, coins_amount):
		self.coins = self.coins - coins_amount
		self.save()

	def spend_pd(self, pd_amount):
		self.pd = self.pd - pd_amount
		self.save()

	def __str__(self):
		return self.user.username

class Item(models.Model):
	name = models.CharField(max_length=140)
	image = models.CharField(max_length=140)
	category = models.CharField(max_length=140)
	description = models.CharField(max_length=256, blank=True, null=True)

	associated_pokemon = models.ForeignKey('pokedex.Pokemon', blank=True, null=True)

	purchase_value = models.IntegerField(default=0)
	purchase_value_coins = models.IntegerField(default=0)
	sell_value = models.IntegerField(default=0)

	def __str__(self):
		return self.name

class Inventory(models.Model):
	user = models.ForeignKey('auth.User')
	item = models.ForeignKey(Item)
	quantity = models.IntegerField(default=1)

	def change_quantity(self, new_quantity):
		self.quantity = new_quantity
		self.save()

	def __str__(self):
		return self.user.username + "'s " + self.item.name

class About(models.Model):
	user = models.ForeignKey('auth.User')
	about = models.TextField(default="Hi! I haven't edited my about section.", blank=True, null=True)

	def __str__(self):
		return "About " + self.user.username




















