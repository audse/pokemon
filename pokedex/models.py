from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

# Create your models here.

class Pokemon(models.Model):
	name = models.CharField(max_length=140)
	number = models.IntegerField()

	primary_type = models.CharField(max_length=24)
	secondary_type = models.CharField(max_length=24, blank=True, null=True)

	rarity = models.IntegerField()

	evo_item = models.CharField(max_length=24, blank=True, null=True)
	evo_level = models.IntegerField(blank=True, null=True)
	evo_on_trade = models.BooleanField(default=False)
	evo = models.IntegerField(blank=True, null=True)

	basic = models.BooleanField(default=False)

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
	happiness = models.FloatField(default=0)

	ready_to_evo_by_trade = models.BooleanField(default=False)

	party = models.BooleanField(default=True)
	boxes = models.BooleanField(default=False)
	gts = models.BooleanField(default=False)
	daycare = models.BooleanField(default=False)

	gender = models.BooleanField()
	nature = models.CharField(max_length=24, blank=True, null=True)
	shiny = models.BooleanField(default=False)

	held_item = models.ForeignKey('core.Item', blank=True, null=True, related_name="held_item")
	nickname = models.CharField(max_length=30, blank=True, null=True)

	# contest stats
	cool = models.IntegerField(default=0)
	tough = models.IntegerField(default=0)
	beauty = models.IntegerField(default=0)
	smart = models.IntegerField(default=0)
	cute = models.IntegerField(default=0)

	update_time = models.DateTimeField(default=timezone.now)

	park_adopt = models.BooleanField(default=False)
	daycare_adopt = models.BooleanField(default=False)

	box_time = models.DateTimeField(blank=True, null=True)
	hatch_time = models.DateTimeField(blank=True, null=True)
	hatched_by = models.ForeignKey('auth.User', blank=True, null=True, related_name="hatched_by")
	evolved_by = models.ForeignKey('auth.User', blank=True, null=True, related_name="evolved_by")

	def interact(self, exp_amount):
		if self.hatched is False:
			if self.exp+exp_amount >= self.pokemon.ehp:
				self.exp = self.pokemon.ehp
				self.save()
			else:
				self.exp += exp_amount
				self.save()
		else:
			if self.total_exp:
				if self.exp+exp_amount >= self.total_exp:
					self.exp = self.total_exp
				else:
					self.exp += exp_amount
			self.save()

	def happiness_interact(self, amount):
		if (self.happiness+amount) > 100:
			self.happiness = 100
		else:
			self.happiness = self.happiness + amount
		self.save()

	def hatch(self, gender, shiny, nature, user):
		self.hatched=True
		self.exp = 0
		self.gender = gender
		self.shiny = shiny
		self.nature = nature
		self.hatch_time = timezone.now()
		self.hatched_by = user
		self.save()

	def evolve(self, evolution, user):
		self.pokemon = evolution
		self.exp = 0
		self.evolved_by = user
		self.save()

	def from_party_to_box(self):
		self.party = False
		self.boxes = True
		self.box_time = timezone.now()
		self.save()

	def from_box_to_party(self):
		self.party = True
		self.boxes = False
		self.box_time = None
		self.save()

	def change_owner(self, new_owner):
		self.owner = new_owner
		self.update_time = timezone.now()
		self.party = True
		self.boxes = False
		self.box_time = None
		self.save()

	def change_nickname(self, new_nickname):
		self.nickname = new_nickname
		self.save()

	def __str__(self):
		name = self.owner.username + "'s " + self.pokemon.name
		if not self.hatched:
			name = name + " egg"
		return name

class Lab(models.Model):
	user = models.ForeignKey('auth.User')

	egg_1 = models.IntegerField()
	egg_2 = models.IntegerField()
	egg_3 = models.IntegerField()
	egg_4 = models.IntegerField()

	create_time = models.DateTimeField(default=timezone.now)
	update_time = models.DateTimeField(default=timezone.now)

	def update(self, egg_1, egg_2, egg_3, egg_4):
		self.egg_1 = egg_1
		self.egg_2 = egg_2
		self.egg_3 = egg_3
		self.egg_4 = egg_4
		self.update_time = timezone.now()
		self.save()

	def __str__(self):
		return self.user.username

class Interaction(models.Model):
	sending_user = models.ForeignKey('auth.User')
	recieving_user = models.CharField(max_length=30)

	adopt = models.ForeignKey(Adopt)
	time = models.DateTimeField(default=timezone.now)

	berry = models.BooleanField(default=False)

	def __str__(self):
		name = self.sending_user.username + " @ " + self.recieving_user + "'s " + self.adopt.pokemon.name
		return name

class Box(models.Model):
	user = models.ForeignKey('auth.User')
	pokemon = models.ManyToManyField(Adopt, blank=True)

	name = models.CharField(max_length=140)
	wallpaper = models.CharField(max_length=6, default="f3d054")

	create_time = models.DateTimeField(default=timezone.now)

	def add_pokemon(self, pokemon):
		self.pokemon.add(pokemon)
		self.save()

	def remove_pokemon(self, pokemon):
		self.pokemon.remove(pokemon)
		self.save()

	def __str__(self):
		name = self.user.username + "'s box, '" + self.name + "'"
		return name

class Dex(models.Model):
	user = models.ForeignKey('auth.User')
	eggs = models.ManyToManyField(Pokemon, blank=True, related_name='eggs')
	pokemon = models.ManyToManyField(Pokemon, blank=True, related_name='pokemon')

	def add_egg_entry(self, egg):
		self.eggs.add(egg)
		self.save()

	def add_pokemon_entry(self, pokemon):
		self.pokemon.add(pokemon)
		self.save()

	def __str__(self):
		name = self.user.username + "'s Dex"
		return name

class Hunt(models.Model):
	user = models.ForeignKey('auth.User')
	pokemon = models.ForeignKey(Pokemon, related_name='hunting_pokemon')
	second_pokemon = models.ForeignKey(Pokemon, related_name='second_hunting_pokemon', blank=True, null=True)

	charge = models.IntegerField(default=0)
	hatched = models.IntegerField(default=0)
	second_hatched = models.IntegerField(default=0)

	reset = models.BooleanField(default=True)

	def add_charge(self, amount):
		if (self.charge + amount) < 300:
			self.charge = self.charge + amount
		else:
			self.charge = 300
		self.save()

	def remove_charge(self, amount):
		self.charge = self.charge - amount
		self.save()

	def reset_radar(self):
		self.charge = 0
		self.hatched = 0
		self.reset = True
		self.save()

	def turn_off_reset(self):
		self.reset = False
		self.save()

	def hatch(self):
		self.hatched = self.hatched + 1
		self.save()

	def hatch_second(self):
		self.second_hatched = self.second_hatched + 1
		self.save()

	def add_second_pokemon(self, pokemon):
		self.second_pokemon = pokemon
		self.second_hatched = 0
		self.save()

	def __str__(self):
		name = self.user.username + "'s " + self.pokemon.name + " Hunt"
		return name

class ShinyCharm(models.Model):
	user = models.ForeignKey('auth.User')
	start_time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		name = self.user.username + "'s Shiny Charm"
		return name

class Trade(models.Model):
	sending_user = models.ForeignKey('auth.User', related_name="sending_user")
	recieving_user = models.ForeignKey('auth.User', related_name="receiving_user")
	sending_adopt = models.ForeignKey(Adopt, related_name="sending_adopt")
	recieving_adopt = models.ForeignKey(Adopt, blank=True, null=True, related_name="recieving_adopt")
	sending_message = models.CharField(max_length=140, blank=True, null=True)
	recieving_message = models.CharField(max_length=140, blank=True, null=True)

	seen_trade = models.BooleanField(default=False)
	seen_offer = models.BooleanField(default=False)
	seen_final = models.BooleanField(default=False)
	
	accepted = models.BooleanField(default=False)
	rejected = models.BooleanField(default=False)

	def add_offer(self, adopt, message):
		self.recieving_adopt = adopt
		self.recieving_message = message
		self.seen_trade = True
		self.save()

	def __str__(self):
		name = self.sending_user.username + "'s trade with " + self.recieving_user.username
		return name

class Contract(models.Model):
	user = models.ForeignKey('auth.User')
	requested_pokemon = models.ForeignKey(Pokemon)
	requested_stat = models.CharField(max_length=24, blank=True, null=True)
	requested_stat_value = models.IntegerField(blank=True, null=True)
	requested_happiness = models.IntegerField(blank=True, null=True)
	difficulty = models.IntegerField()

	date_accepted = models.DateTimeField(default=timezone.now)

	payment_method = models.CharField(max_length=24, default="PD")
	payment_amount = models.IntegerField()

	def __str__(self):
		name = "Requesting " + self.requested_pokemon.name + " from " + self.user.username
		return name

class PotentialContract(models.Model):
	user = models.ForeignKey('auth.User')
	difficulty = models.IntegerField()

	def __str__(self):
		name = "Difficulty " + self.difficulty + " contract for " + self.user.username
		return name

class DaycareEgg(models.Model):
	user = models.ForeignKey('auth.User')
	pokemon = models.ForeignKey('Pokemon')

	def __str__(self):
		name = self.user.username + " 's " + self.pokemon.name + " egg"
		return name











