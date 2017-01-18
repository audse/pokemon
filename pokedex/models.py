from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

# Create your models here.

class Pokemon(models.Model):
	name = models.CharField(max_length=140)
	number = models.IntegerField()

	primary_type = models.CharField(max_length=24)
	secondary_type = models.CharField(max_length=24, blank=True, null=True)

	evo_item = models.CharField(max_length=24, blank=True, null=True)
	evo_level = models.IntegerField(blank=True, null=True)
	evo_on_trade = models.BooleanField(default=False)
	evo = models.IntegerField(blank=True, null=True)

	rate = models.CharField(max_length=24)

	percent_male = models.IntegerField()
	ehp = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return str(self.number)+" "+self.name

class Adopt(models.Model):
	pokemon = models.ForeignKey('Pokemon')
	owner = models.ForeignKey('auth.User')

	hatched = models.BooleanField(default=False)
	exp = models.IntegerField(default=0)
	total_exp = models.IntegerField(blank=True, null=True)
	happiness = models.IntegerField(default=0)

	party = models.BooleanField(default=True)
	boxes = models.BooleanField(default=False)
	box_x_coord = models.IntegerField(blank=True, null=True)
	box_y_coord = models.IntegerField(blank=True, null=True)

	gender = models.BooleanField()
	nature = models.CharField(max_length=24, blank=True, null=True)
	shiny = models.BooleanField(default=False)

	held_item = models.CharField(max_length=140, blank=True, null=True)
	nickname = models.CharField(max_length=30, blank=True, null=True)

	def interact(self, exp_amount):
		if self.hatched is False:
			if self.exp+exp_amount >= self.pokemon.ehp:
				self.exp = self.pokemon.ehp
				self.save()
			else:
				self.exp += exp_amount
				self.save()
		else:
			self.exp += exp_amount
			self.save()

	def hatch(self, gender, shiny, nature):
		self.hatched=True
		self.exp = 0
		self.gender = gender
		self.shiny = shiny
		self.nature = nature
		self.save()

	def __str__(self):
		name = self.owner.username + "'s " + self.pokemon.name
		return name

class Lab(models.Model):
	user = models.ForeignKey('auth.User')

	egg_1 = models.IntegerField()
	egg_2 = models.IntegerField()
	egg_3 = models.IntegerField()
	egg_4 = models.IntegerField()

	create_time = models.DateTimeField(default=timezone.now)

	def update(self, egg_1, egg_2, egg_3, egg_4):
		self.egg_1 = egg_1
		self.egg_2 = egg_2
		self.egg_3 = egg_3
		self.egg_4 = egg_4
		self.save()

class Interaction(models.Model):
	sending_user = models.ForeignKey('auth.User')
	recieving_user = models.CharField(max_length=30)

	adopt = models.ForeignKey(Adopt)
	time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		name = self.sending_user.username + " @ " + self.recieving_user
		return name

class Box(models.Model):
	user = models.ForeignKey('auth.user')
	pokemon = models.ManyToManyField(Adopt)

	name = models.CharField(max_length=140)
	wallpaper = models.IntegerField(default=1)

	def __str__(self):
		name = self.user.username + "'s box, '" + self.name + "'"
		return name











