from django.shortcuts import render
from .models import Pokemon
from core import views as core_views

# Create your views here.
def index(request):
	action = "Viewing the Pok&eacute;dex"
	core_views.update_online(request, action)

	pokemon = Pokemon.objects.all()
	for monster in pokemon:
		monster.percent_female = 100 - monster.percent_male

	return render(request, 'pokedex/index.html', {'pokemon':pokemon})