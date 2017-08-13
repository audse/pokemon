from django.template import Library

from pokedex.models import Dex

register = Library()

@register.filter(name="rank")
def rank(user):
	dex = Dex.objects.filter(user=user)
	if dex.count() != 0:
		dex = dex.first()
		dex_entries = dex.pokemon.count()
		egg_entries = dex.eggs.count()

		if dex_entries >= 150 and egg_entries >= 75:
			rank = 1
		elif dex_entries >= 100 and egg_entries >= 50:
			rank = 2
		elif dex_entries >= 40 and egg_entries >= 20:
			rank = 3
		elif dex_entries >= 10 and egg_entries >= 5:
			rank = 4
		else:
			rank = 5

		return rank
	else:
		return 5