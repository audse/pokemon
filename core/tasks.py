import datetime
import celery
from celery.task.schedules import crontab

from django.contrib.auth.models import User
from pokedex.models import Adopt, DaycareEgg

# @celery.decorators.periodic_task(run_every=datetime.timedelta(seconds=10))
@celery.decorators.periodic_task(run_every=crontab(hour=0, minute=0))
def lose_happiness_every_day():
	adopts = Adopt.objects.filter(hatched=True)
	for adopt in adopts:
		if adopt.happiness > 1:
			adopt.happiness -= 1
			adopt.save()
		else:
			adopt.happiness = 0
			adopt.save() 

@celery.decorators.periodic_task(run_every=crontab(hour=0, minute=0))
def create_daycare_eggs():
	# first, release all unclaimed eggs to park
	daycare_eggs = DaycareEgg.objects.all()
	cedar = User.objects.filter(username="CEDAR")
	for egg in daycare_eggs:
		total_exp = 0
		multiplier = 1
		if egg.pokemon.evo_level is not None:
			total_exp = egg.evo_level*1000
			multiplier = 1
			if egg.pokemon.rate == "slow":
				multiplier = 2
			elif egg.pokemon.rate == "medium slow":
				multiplier = 1.5
			elif egg.pokemon.rate == "medium fast":
				multiplier = 1
			elif egg.pokemon.rate == "fast":
				multiplier = .7

			total_exp*=multiplier

			adopt = Adopt.objects.create(owner=cedar, pokemon=egg.pokemon, hatched=False, exp=0, happiness=0, gender=True, total_exp=total_exp)
			egg.delete()

	# then, generate daycare eggs for compatible adopts
	all_users = User.objects.all()
	for user in all_users:
		daycare_adopts = Adopt.objects.filter(owner=user, daycare=True)
		if daycare_adopts.count() == 2:
			if daycare_adopts[0].pokemon == daycare_adopts[1].pokemon:
				if (daycare_adopts[0].gender and not daycare_adopts[1].gender) or (daycare_adopts[1].gender and not daycare_adopts[0].gender):
					rate = daycare_adopts[0].pokemon.rarity
					eggs = 0
					if rate == 1:
						eggs = 8
					elif rate == 2:
						eggs = 6
					elif rate == 3:
						eggs = 3
					elif rate == 4:
						eggs = 2
					elif rate == 5:
						eggs = 1

					for i in range(0, eggs):
						daycare_egg = DaycareEgg.objects.create(user=user, pokemon=daycare_adopts[0].pokemon)











