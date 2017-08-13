from __future__ import division
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string


from django.contrib.auth.models import User
from .models import Action, Currency, Item, Inventory, About
from pokedex.models import Pokemon, Adopt, Lab, Interaction, Box, Dex, Hunt, Trade, Contract, PotentialContract, ShinyCharm, DaycareEgg

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import datetime
from datetime import timedelta, time
from datetime import datetime as dt_datetime
from django.utils import timezone
import random

from lxml import etree
import urllib2

# FUNCTIONS

def update_online(request, action="Viewing Pok&eacute;monPC", override=False):
	if request.user.is_authenticated():
		action_account = Action.objects.filter(user=request.user)
		if action_account.count() is not 0:
			if not request.user.is_superuser:
				action_account = action_account.first()
				action_account.update(action)
			else:
				if override:
					action_account = action_account.first()
					action_account.update(action)
				else:
					action_account = action_account.first()
					action_account.update_time()
		else:
			action_account = Action.objects.create(user=request.user, action=action)
			action_account.save()

"""
def get_likes(adopt):
	adopt.favorite = "any"
	adopt.disliked = "any"

	# likes spicy
	if adopt.nature == "adamant":
		adopt.favorite = "spicy"
		adopt.disliked = "dry"

	elif adopt.nature == "brave":
		adopt.favorite = "spicy"
		adopt.disliked = "sweet"

	elif adopt.nature == "naughty":
		adopt.favorite = "spicy"
		adopt.disliked = "bitter"

	elif adopt.nature == "lonely":
		adopt.favorite = "spicy"
		adopt.disliked = "sour"

	# likes dry
	elif adopt.nature == "modest":
		adopt.favorite = "dry"
		adopt.disliked = "spicy"

	elif adopt.nature == "quiet":
		adopt.favorite = "dry"
		adopt.disliked = "sweet"

	elif adopt.nature == "rash":
		adopt.favorite = "dry"
		adopt.disliked = "bitter"

	elif adopt.nature == "mild":
		adopt.favorite = "dry"
		adopt.disliked = "sour"

	# likes sweet
	elif adopt.nature == "timid":
		adopt.favorite = "sweet"
		adopt.disliked = "spicy"
		
	elif adopt.nature == "jolly":
		adopt.favorite = "sweet"
		adopt.disliked = "dry"

	elif adopt.nature == "naive":
		adopt.favorite = "sweet"
		adopt.disliked = "bitter"
		
	elif adopt.nature == "hasty":
		adopt.favorite = "sweet"
		adopt.disliked = "sour"

	# likes bitter
	elif adopt.nature == "calm":
		adopt.favorite = "bitter"
		adopt.disliked = "spicy"
		
	elif adopt.nature == "careful":
		adopt.favorite = "bitter"
		adopt.disliked = "dry"

	elif adopt.nature == "sassy":
		adopt.favorite = "bitter"
		adopt.disliked = "sweet"
		
	elif adopt.nature == "quirky":
		adopt.favorite = "bitter"
		adopt.disliked = "sour"

	# likes sour
	elif adopt.nature == "bold":
		adopt.favorite = "sour"
		adopt.disliked = "spicy"
		
	elif adopt.nature == "impish":
		adopt.favorite = "sour"
		adopt.disliked = "dry"

	elif adopt.nature == "relaxed":
		adopt.favorite = "sour"
		adopt.disliked = "sweet"
		
	elif adopt.nature == "lax":
		adopt.favorite = "sour"
		adopt.disliked = "bitter"


	# likes spicy
	if adopt.nature == "adamant":
		adopt.favorite = "spicy"
		adopt.disliked = "dry"

	elif adopt.nature == "brave":
		adopt.favorite = "spicy"
		adopt.disliked = "sweet"

	elif adopt.nature == "naughty":
		adopt.favorite = "spicy"
		adopt.disliked = "bitter"

	elif adopt.nature == "lonely":
		adopt.favorite = "spicy"
		adopt.disliked = "sour"

	# likes dry
	elif adopt.nature == "modest":
		adopt.favorite = "dry"
		adopt.disliked = "spicy"

	elif adopt.nature == "quiet":
		adopt.favorite = "dry"
		adopt.disliked = "sweet"

	elif adopt.nature == "rash":
		adopt.favorite = "dry"
		adopt.disliked = "bitter"

	elif adopt.nature == "mild":
		adopt.favorite = "dry"
		adopt.disliked = "sour"

	# likes sweet
	elif adopt.nature == "timid":
		adopt.favorite = "sweet"
		adopt.disliked = "spicy"
		
	elif adopt.nature == "jolly":
		adopt.favorite = "sweet"
		adopt.disliked = "dry"

	elif adopt.nature == "naive":
		adopt.favorite = "sweet"
		adopt.disliked = "bitter"
		
	elif adopt.nature == "hasty":
		adopt.favorite = "sweet"
		adopt.disliked = "sour"

	# likes bitter
	elif adopt.nature == "calm":
		adopt.favorite = "bitter"
		adopt.disliked = "spicy"
		
	elif adopt.nature == "careful":
		adopt.favorite = "bitter"
		adopt.disliked = "dry"

	elif adopt.nature == "sassy":
		adopt.favorite = "bitter"
		adopt.disliked = "sweet"
		
	elif adopt.nature == "quirky":
		adopt.favorite = "bitter"
		adopt.disliked = "sour"

	# likes sour
	elif adopt.nature == "bold":
		adopt.favorite = "sour"
		adopt.disliked = "spicy"
		
	elif adopt.nature == "impish":
		adopt.favorite = "sour"
		adopt.disliked = "dry"

	elif adopt.nature == "relaxed":
		adopt.favorite = "sour"
		adopt.disliked = "sweet"
		
	elif adopt.nature == "lax":
		adopt.favorite = "sour"
		adopt.disliked = "bitter"
"""

def check_interaction(user, adopt):
	if not adopt.hatched:
		adopt.percent = adopt.exp/adopt.pokemon.ehp*100
	else:
		if adopt.pokemon.evo_level:
			if adopt.total_exp is not 0:
				adopt.percent = adopt.exp/adopt.total_exp*100
			else:
				adopt.percent = 100
		else:
			adopt.percent = 100

	# make sure they havent interacted in the past day
	if user.is_authenticated():
		# time_threshold = datetime.datetime.now() - timedelta(hours=1)
		today = dt_datetime.now().date()
		interactions_since_yesterday = Interaction.objects.filter(recieving_user=adopt.owner.username, sending_user=user, adopt=adopt, time__gte=today).count()
		if interactions_since_yesterday is not 0:
			adopt.can_interact = False
		else:
			adopt.can_interact = True

def manually_update_online(request):
	if request.user.is_authenticated():
		if request.user.is_superuser:
			action = str(request.POST.get("action"))
			update_online(request, action, True)
			return redirect(profile_page, username=request.user.username)
		else:
			return redirect(staff_only)
	else:
		return redirect(must_be_logged_in)



# STATIC PAGES

def index(request):
	if request.user.is_authenticated():
		if not request.user.is_superuser:
			action = "Viewing the home page"
			action_account = Action.objects.filter(user=request.user)
			if action_account.count() is not 0:
				action_account = action_account.first()
				action_account.update(action)

	return render(request, 'core/index.html')

def login_page(request):
	return render(request, 'core/login.html')

def register_page(request):
	return render(request, 'core/register.html')

def profile_page(request, username):

	action = "Viewing "+username+"'s profile"
	update_online(request, action)

	user_exists = User.objects.filter(username=username)

	if user_exists.count() is not 0:
		user = user_exists.first()

		if user.username != "CEDAR":
			adopts = Adopt.objects.filter(owner=user, party=True, gts=False, daycare=False).order_by('update_time')
			for adopt in adopts:
				check_interaction(request.user, adopt)
		else:
			return redirect(lab)

		boxes = Box.objects.filter(user=user)

		about = About.objects.get(user=user)

		if request.user.is_authenticated():
			aguav_berry_item = Item.objects.filter(image="aguav-berry")
			has_aguav_berry = Inventory.objects.filter(user=request.user, item=aguav_berry_item).count()

			leppa_berry_item = Item.objects.filter(image="leppa-berry")
			has_leppa_berry = Inventory.objects.filter(user=request.user, item=leppa_berry_item).count()

			kasib_berry_item = Item.objects.filter(image="kasib-berry")
			has_kasib_berry = Inventory.objects.filter(user=request.user, item=kasib_berry_item).count()

			chesto_berry_item = Item.objects.filter(image="chesto-berry")
			has_chesto_berry = Inventory.objects.filter(user=request.user, item=chesto_berry_item).count()

			sitrus_berry_item = Item.objects.filter(image="sitrus-berry")
			has_sitrus_berry = Inventory.objects.filter(user=request.user, item=sitrus_berry_item).count()
		else: 
			has_aguav_berry = False
			has_leppa_berry = False
			has_kasib_berry = False
			has_chesto_berry = False
			has_sitrus_berry = False

		return render(request, 'core/profile.html', {'current_user':user, 'about':about, 'adopts':adopts, 'boxes': boxes, 'has_aguav_berry':has_aguav_berry, 'has_leppa_berry':has_leppa_berry, 'has_kasib_berry':has_kasib_berry, 'has_chesto_berry':has_chesto_berry, 'has_sitrus_berry':has_sitrus_berry})
	else:
		return redirect(user_not_found)

def load_box(request, pk):
	box = Box.objects.get(pk=pk)
	return render(request, 'includes/load_box.html', {'box':box})

def edit_about(request):
	if request.user.is_authenticated():
		about_text = request.POST.get("about_text")
		about = About.objects.get(user=request.user)
		about.about = about_text
		about.save()
		return redirect(profile_page, username=request.user.username)
	else:
		return render(must_be_logged_in)

def online_page(request):

	action = "Viewing the online users list"
	update_online(request, action)

	# get list of currently online users
	machine = User.objects.get(username="CEDAR")
	time_threshold = datetime.datetime.now() - timedelta(minutes=10)
	online_users = Action.objects.filter(time__gte=time_threshold).filter(online=True).exclude(user=machine).order_by('-time')

	# paginate to display X amount of users per page
	paginator = Paginator(online_users, 20)
	page = request.GET.get('page')
	try:
		online_users = paginator.page(page)
	except PageNotAnInteger:
		online_users = paginator.page(1)
	except EmptyPage:
		online_users = paginator.page(paginator.num_pages)

	return render(request, 'core/online.html', {'online_users':online_users})



# FUNCTIONAL VIEWS

def login(request):
	action = "Logging in"
	update_online(request, action)

	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)

	if user is not None: # success
		auth_login(request, user)
		return redirect(profile_page, username=username)
	else: # failure
		return redirect(login_failed)

def logout(request):
	if request.user.is_authenticated():
		action_account = Action.objects.filter(user=request.user)
		if action_account.count() is not 0:
			action_account = action_account.first()
			action_account.offline()


	auth_logout(request)
	return redirect(index)
	
def register(request):
	if request.user.is_authenticated():
		return redirect(cannot_be_logged_in)
	else:
		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		age = request.POST.get('age')

		errors = []

		all_fields_filled_out = False
		username_not_in_use = True
		email_not_in_use = True
		passwords_are_same = True

		# check that all fields are filled out
		if username and password and confirm_password and email and age:
			all_fields_filled_out = True
		else:
			errors.append("Make sure that all fields are filled out and that you are over 13.")
			all_fields_filled_out = False

		# check that username is not being used
		if User.objects.filter(username=username).count() is not 0:
			errors.append("That username is already in use. Please choose something else!")
			username_not_in_use = False
		else:
			username_not_in_use = True

		# check that email is not being used
		if User.objects.filter(email=email).count() is not 0:
			errors.append("That email is already in use. Make sure you haven't already signed up! Alt accounts are against our terms of service.")
			email_not_in_use = False
		else:
			email_not_in_use = True

		# check that passwords match
		if password == confirm_password:
			passwords_are_same = True
		else:
			if all_fields_filled_out:
				errors.append("The passwords entered don't match.")
			passwords_are_same = False

		# check that everything is correct
		if all_fields_filled_out and username_not_in_use and email_not_in_use and passwords_are_same:
			user = User.objects.create_user(username=username, email=email, password=password)
			account_currency = Currency.objects.create(user=user)
			about = About.objects.create(user=user)
			user.save()
			account_currency.save()
			about.save()
			return redirect(index)
		else:
			return render(request, 'core/register.html', {'errors':errors})



# ERROR VIEWS

def must_be_logged_in(request):
	return render(request, 'error/must_be_logged_in.html')

def cannot_be_logged_in(request):
	return render(request, 'error/cannot_be_logged_in.html')

def user_not_found(request):
	return render(request, 'error/user_not_found.html')

def login_failed(request):
	return render(request, 'error/login_failed.html')

def cannot_interact(request):
	return render(request, 'error/cannot_interact.html')

def pokemon_not_found(request):
	return render(request, 'error/pokemon_not_found.html')

def cannot_access(request):
	return render(request, 'error/cannot_access.html')

def staff_only(request):
	return render(request, 'error/staff_only.html')

def party_is_full(request):
	return render(request, 'error/party_is_full.html')

# EVENT VIEWS

def check_yesterday_interactions():
	today = dt_datetime.now().date()

	yesterday = today - timedelta(1)
	yesterday_start = dt_datetime.combine(yesterday, time())
	yesterday_end = dt_datetime.combine(today, time())

	day_before = today - timedelta(2)
	day_before_start = dt_datetime.combine(day_before, time())
	day_before_end = dt_datetime.combine(yesterday, time())

	yesterday_interactions = Interaction.objects.filter(time__gte=yesterday_start, time__lte=yesterday_end).count()
	day_before_interactions = Interaction.objects.filter(time__gte=day_before_start, time__lte=day_before_end).count()

	if yesterday_interactions >= 2000:
		if day_before_interactions >= 2000:
			return False # no two days in a row
		else:
			return True
	else:
		return False

def check_yesterday_berry_interactions():
	today = dt_datetime.now().date()

	yesterday = today - timedelta(1)
	yesterday_start = dt_datetime.combine(yesterday, time())
	yesterday_end = dt_datetime.combine(today, time())

	day_before = today - timedelta(2)
	day_before_start = dt_datetime.combine(day_before, time())
	day_before_end = dt_datetime.combine(yesterday, time())

	yesterday_berry_interactions = Interaction.objects.filter(time__gte=yesterday_start, time__lte=yesterday_end, berry=True).count()
	day_before_berry_interactions = Interaction.objects.filter(time__gte=day_before_start, time__lte=day_before_end, berry=True).count()

	if yesterday_berry_interactions >= 500:
		if day_before_berry_interactions >= 500:
			return False # no two days in a row
		else:
			return True
	else:
		return False

def check_yesterday_hatched():
	today = dt_datetime.now().date()

	yesterday = today - timedelta(1)
	yesterday_start = dt_datetime.combine(yesterday, time())
	yesterday_end = dt_datetime.combine(today, time())

	day_before = today - timedelta(2)
	day_before_start = dt_datetime.combine(day_before, time())
	day_before_end = dt_datetime.combine(yesterday, time())

	yesterday_hatched = Adopt.objects.filter(hatch_time__gte=yesterday_start, hatch_time__lte=yesterday_end).count()
	day_before_hatched = Adopt.objects.filter(hatch_time__gte=day_before_start, hatch_time__lte=day_before_end).count()

	if yesterday_hatched >= 100:
		if day_before_hatched >= 100:
			return False # no two days in a row
		else:
			return True
	else:
		return False

def todays_interactions(request):
	if request.user.is_authenticated():
		action = "Viewing today's interactions"
		update_online(request, action)

		today = dt_datetime.now().date()
		tomorrow = today + timedelta(1)
		today_start = dt_datetime.combine(today, time())
		today_end = dt_datetime.combine(tomorrow, time())

		interactions = Interaction.objects.filter(time__gte=today_start, time__lte=today_end).count()
		berry_interactions = Interaction.objects.filter(time__gte=today_start, time__lte=today_end, berry=True).count()
		hatched = Adopt.objects.filter(hatch_time__gte=today_start, hatch_time__lte=today_end).count()

		interaction_quota = 2000
		berry_quota = 500
		hatch_quota = 100

		interaction_progress = 0
		berry_progress = 0
		hatch_progress = 0


		yesterday_interactions_met = False
		yesterday_berry_interactions_met = False
		yesterday_hatched_met = False

		if not check_yesterday_interactions():
			interaction_progress = (interactions/interaction_quota)*100
			if interaction_progress > 100.0:
				interaction_progress = 100.0
		else:
			yesterday_interactions_met = True

		if not check_yesterday_berry_interactions():
			berry_progress = (berry_interactions/berry_quota)*100
			if berry_progress > 100.0:
				berry_progress = 100.0
		else:
			yesterday_berry_interactions_met = True

		if not check_yesterday_hatched():
			hatch_progress = (hatched/hatch_quota)*100
			if hatch_progress > 100.0:
				hatch_progress = 100.0
		else:
			yesterday_hatched_met = True


		your_interactions = Interaction.objects.filter(sending_user=request.user, time__gte=today_start, time__lte=today_end).count()
		your_overall_interactions = Interaction.objects.filter(sending_user=request.user).count()
		your_berry_interactions = Interaction.objects.filter(sending_user=request.user, time__gte=today_start, time__lte=today_end, berry=True).count()
		your_interactions_contribution = round((your_interactions/interactions)*100, 1)

		clickback = Interaction.objects.filter(recieving_user=request.user.username, time__gte=today_start, time__lte=today_end)
		clickback_users = []

		for click in clickback:
			if click.sending_user in clickback_users:
				pass
			else:
				clickback_users.append(click.sending_user)

		clicked = Interaction.objects.filter(sending_user=request.user, time__gte=today_start, time__lte=today_end)
		clicked_users = []

		for click in clicked:
			recieving_user = User.objects.filter(username=click.recieving_user).first()
			if recieving_user in clicked_users:
				pass
			else:
				clicked_users.append(recieving_user)

		users_to_click = set(clickback_users).difference(set(clicked_users))

		# raise ValueError(str(clickback_user_count) + " - " + str(clicked_user_count))

		return render(request, 'core/todays_interactions.html', {'interactions':interactions, 'berry_interactions':berry_interactions, 'hatched':hatched, 'interaction_progress':interaction_progress, 'berry_progress':berry_progress, 'hatch_progress':hatch_progress, 'your_interactions':your_interactions, 'your_overall_interactions':your_overall_interactions, 'your_berry_interactions':your_berry_interactions, 'your_interactions_contribution':your_interactions_contribution, 'users_to_click':users_to_click, 'yesterday_interactions_met':yesterday_interactions_met, 'yesterday_berry_interactions_met':yesterday_berry_interactions_met, 'yesterday_hatched_met':yesterday_hatched_met})
	else:
		return redirect(must_be_logged_in)

# LAB VIEWS

def update_lab(request):
	lab_set = Lab.objects.get(user=request.user)
	if lab_set:

		rarity_level = []
		rarities = []

		for x in range(0, 4):
			rarities.append(random.randint(1, 991))

		for rarity in rarities:
			if rarity < 700:
				rarity_level.append(1)
			elif rarity < 910:
				rarity_level.append(2)
			elif rarity < 973:
				rarity_level.append(3)
			elif rarity < 992:
				rarity_level.append(4)

		egg_1 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[0]).order_by('?').first().number
		egg_2 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[1]).order_by('?').first().number
		egg_3 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[2]).order_by('?').first().number
		egg_4 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[3]).order_by('?').first().number
		lab_set.update(egg_1=egg_1, egg_2=egg_2, egg_3=egg_3, egg_4=egg_4)

def lab(request):
	if request.user.is_authenticated():
		action = "Visiting the lab"
		update_online(request, action)

		check_for_dex = Dex.objects.filter(user=request.user)
		if check_for_dex.count() != 0:
			lab_set = Lab.objects.filter(user=request.user).first()
			if lab_set:
				lab_set.egg_1_type = Pokemon.objects.get(number=lab_set.egg_1).primary_type
				lab_set.egg_2_type = Pokemon.objects.get(number=lab_set.egg_2).primary_type
				lab_set.egg_3_type = Pokemon.objects.get(number=lab_set.egg_3).primary_type
				lab_set.egg_4_type = Pokemon.objects.get(number=lab_set.egg_4).primary_type

				dex = check_for_dex.first()
				dex_entries = dex.pokemon.count()
				egg_entries = dex.eggs.count()

				summons = Item.objects.filter(category="summon")
				fossils = Item.objects.filter(category="fossil")
				inventory = Inventory.objects.filter(user=request.user)

				return render(request, 'site/lab.html', {'lab_set':lab_set, 'dex_entries':dex_entries, 'egg_entries':egg_entries, 'summons':summons, 'fossils':fossils, 'inventory':inventory})
			else:

				rarity_level = []
				rarities = []

				for x in range(0, 4):
					rarities.append(random.randint(1, 991))

				for rarity in rarities:
					if rarity < 700:
						rarity_level.append(1)
					elif rarity < 910:
						rarity_level.append(2)
					elif rarity < 973:
						rarity_level.append(3)
					elif rarity < 992:
						rarity_level.append(4)

				egg_1 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[0]).order_by('?').first().number
				egg_2 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[1]).order_by('?').first().number
				egg_3 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[2]).order_by('?').first().number
				egg_4 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[3]).order_by('?').first().number
				lab_set = Lab.objects.create(user=request.user, egg_1=egg_1, egg_2=egg_2, egg_3=egg_3, egg_4=egg_4)
				lab_set.save()
				lab_set.egg_1_type = Pokemon.objects.get(number=lab_set.egg_1).primary_type
				lab_set.egg_2_type = Pokemon.objects.get(number=lab_set.egg_2).primary_type
				lab_set.egg_3_type = Pokemon.objects.get(number=lab_set.egg_3).primary_type
				lab_set.egg_4_type = Pokemon.objects.get(number=lab_set.egg_4).primary_type

				dex = check_for_dex.first()
				dex_entries = dex.pokemon.count()
				egg_entries = dex.eggs.count()

				summons = Item.objects.filter(category="summon")
				fossils = Item.objects.filter(category="fossil")
				inventory = Inventory.objects.filter(user=request.user)

				return render(request, 'site/lab.html', {'lab_set':lab_set, 'dex_entries':dex_entries, 'egg_entries':egg_entries, 'summons':summons, 'fossils':fossils, 'inventory':inventory})
		else:
			return render(request, 'site/lab_new_user.html')
	else:
		return render(request, 'site/lab.html')

def lab_reload(request):
	if request.user.is_authenticated():
		update_lab(request)
		return redirect(lab)
	else:
		return redirect(must_be_logged_in)

def lab_adopt(request, pk):
	if request.user.is_authenticated():
		lab_set = Lab.objects.get(user=request.user)
		lab_egg = 129

		if pk == "1":
			lab_egg = lab_set.egg_1
		elif pk == "2":
			lab_egg = lab_set.egg_2
		elif pk == "3":
			lab_egg = lab_set.egg_3
		elif pk == "4":
			lab_egg = lab_set.egg_4
		else:
			return redirect(lab)

		egg = Pokemon.objects.get(number=lab_egg)

		amount_in_party = Adopt.objects.filter(owner=request.user, party=True, daycare=False, gts=False).count()
		if amount_in_party < 6:

			total_exp = 0
			multiplier = 1
			if egg.evo_level is not None:
				total_exp = egg.evo_level*1000
				multiplier = 1
				if egg.rate == "slow":
					multiplier = 2
				elif egg.rate == "medium slow":
					multiplier = 1.5
				elif egg.rate == "medium fast":
					multiplier = 1
				elif egg.rate == "fast":
					multiplier = .7

				total_exp*=multiplier

			adopt = Adopt.objects.create(owner=request.user, pokemon=egg, hatched=False, exp=0, happiness=0, gender=True, total_exp=total_exp)
			update_lab(request)
			return redirect(profile_page, username=request.user.username)
		else:
			return redirect(party_is_full)
	else:
		return redirect(must_be_logged_in)

def summon_pokemon(request, item_pk):
	if request.user.is_authenticated():
		check_for_dex = Dex.objects.filter(user=request.user)
		if check_for_dex.count() != 0:
			dex = check_for_dex.first()
			dex_entries = dex.pokemon.count()
			egg_entries = dex.eggs.count()
			if dex_entries >= 50 and egg_entries >= 30:
				has_item = Inventory.objects.filter(pk=item_pk)
				if has_item.count() != 0:
					item = has_item.first()
					if item.user == request.user:

						amount_in_party = Adopt.objects.filter(owner=request.user, party=True, daycare=False, gts=False).count()
						if amount_in_party < 6:
							if item.quantity > 1:
								item.quantity -= 1
								item.save()
							else:
								item.delete()

							# generate adopt

							total_exp = 0
							multiplier = 1
							if item.item.associated_pokemon.evo_level is not None:
								total_exp = item.item.associated_pokemon.evo_level*1000
								multiplier = 1
								if item.item.associated_pokemon.rate == "slow":
									multiplier = 2
								elif item.item.associated_pokemon.rate == "medium slow":
									multiplier = 1.5
								elif item.item.associated_pokemon.rate == "medium fast":
									multiplier = 1
								elif item.item.associated_pokemon.rate == "fast":
									multiplier = .7

								total_exp*=multiplier

							adopt = Adopt.objects.create(owner=request.user, pokemon=item.item.associated_pokemon, hatched=False, exp=0, happiness=0, gender=True, total_exp=total_exp)
							return redirect(profile_page, username=request.user.username)
						else:
							return redirect(party_is_full)
					else:
						return redirect(cannot_access)
				else:
					return redirect(lab)
			else:
				return redirect(lab)
		else:
			return redirect(lab)
	else:
		return redirect(must_be_logged_in)


# INTERACTION WITH ADOPTS VIEWS

def interact(request):
	if request.user.is_authenticated():
		action = "Interacting"
		update_online(request, action)

		pk = request.POST.get("pk")
		username = request.POST.get("owner_username")
		berry = request.POST.get("berry")
		recieving_user = User.objects.filter(username=username).first()
		adopt = Adopt.objects.filter(pk=pk).first()
		if recieving_user:
			# find all interactions with this pokemon since yesterday
			# if there are any, do not let interact
			# time_threshold = datetime.datetime.now() - timedelta(hours=1)
			today = dt_datetime.now().date()
			interactions_since_yesterday = Interaction.objects.filter(recieving_user=username, sending_user=request.user, adopt=adopt, time__gte=today).count()
			if interactions_since_yesterday is not 0:
				return redirect(cannot_interact)
			else:

				if check_yesterday_interactions():
					exp_amount = 200
				else:
					exp_amount = 100

				if adopt.party:
					if berry == "smart":
						berry_name = "aguav-berry"
						berry_item = Item.objects.filter(image=berry_name)
						has_berry = Inventory.objects.filter(user=request.user, item=berry_item)
						if has_berry.count() != 0:
							berry_inventory = has_berry.first()
							if berry_inventory.quantity > 1:
								berry_inventory.quantity -= 1
								berry_inventory.save()
							else:
								berry_inventory.delete()
							if adopt.smart <= 95:
								adopt.smart += 5
								adopt.save()
							else:
								adopt.smart = 100
								adopt.save()
						else:
							return redirect(profile_page, username=request.user.username)
					elif berry == "cool":
						berry_name = "leppa-berry"
						berry_item = Item.objects.filter(image=berry_name)
						has_berry = Inventory.objects.filter(user=request.user, item=berry_item)
						if has_berry.count() != 0:
							berry_inventory = has_berry.first()
							if berry_inventory.quantity > 1:
								berry_inventory.quantity -= 1
								berry_inventory.save()
							else:
								berry_inventory.delete()
							if adopt.cool <= 95:
								adopt.cool += 5
								adopt.save()
							else:
								adopt.cool = 100
								adopt.save()
						else:
							return redirect(profile_page, username=request.user.username)
					elif berry == "cute":
						berry_name = "kasib-berry"
						berry_item = Item.objects.filter(image=berry_name)
						has_berry = Inventory.objects.filter(user=request.user, item=berry_item)
						if has_berry.count() != 0:
							berry_inventory = has_berry.first()
							if berry_inventory.quantity > 1:
								berry_inventory.quantity -= 1
								berry_inventory.save()
							else:
								berry_inventory.delete()
							if adopt.cute <= 95:
								adopt.cute += 5
								adopt.save()
							else:
								adopt.cute = 100
								adopt.save()
						else:
							return redirect(profile_page, username=request.user.username)
					elif berry == "beauty":
						berry_name = "chesto-berry"
						berry_item = Item.objects.filter(image=berry_name)
						has_berry = Inventory.objects.filter(user=request.user, item=berry_item)
						if has_berry.count() != 0:
							berry_inventory = has_berry.first()
							if berry_inventory.quantity > 1:
								berry_inventory.quantity -= 1
								berry_inventory.save()
							else:
								berry_inventory.delete()
							if adopt.beauty <= 95:
								adopt.beauty += 5
								adopt.save()
							else:
								adopt.beauty = 100
								adopt.save()
						else:
							return redirect(profile_page, username=request.user.username)
					elif berry == "tough":
						berry_name = "sitrus-berry"
						berry_item = Item.objects.filter(image=berry_name)
						has_berry = Inventory.objects.filter(user=request.user, item=berry_item)
						if has_berry.count() != 0:
							berry_inventory = has_berry.first()
							if berry_inventory.quantity > 1:
								berry_inventory.quantity -= 1
								berry_inventory.save()
							else:
								berry_inventory.delete()
							if adopt.tough <= 95:
								adopt.tough += 5
								adopt.save()
							else:
								adopt.tough = 100
								adopt.save()
						else:
							return redirect(profile_page, username=request.user.username)

				if berry is not None:
					berry_interaction = True
				else:
					berry_interaction = False

				exp_share = Item.objects.filter(image="exp-share").first()
				has_exp_share = Inventory.objects.filter(user=request.user, item=exp_share)
				if has_exp_share.count() != 0:
					party_pokemon = Adopt.objects.filter(owner=request.user, party=True)
					party_exp_amount = exp_amount/5
					for pokemon in party_pokemon:
						pokemon.interact(party_exp_amount)

				if adopt.pokemon.evo_level or not adopt.hatched:
					adopt.interact(exp_amount)
				else:
					adopt.happiness_interact(0.1)
				interaction = Interaction.objects.create(sending_user = request.user, recieving_user=recieving_user, adopt=adopt, berry=berry_interaction)

				amulet_coin_item = Item.objects.get(name="amulet coin")
				has_amulet_coin = Inventory.objects.filter(user=request.user, item=amulet_coin_item)

				users_currency = Currency.objects.filter(user=request.user).first()
				if has_amulet_coin.count() != 0:
					pd_amount = random.randint(5, 10)
				else:
					pd_amount = random.randint(1, 5)
				users_currency.get_pd(pd_amount)

				check_for_radar = Hunt.objects.filter(user=request.user)
				if check_for_radar.count() != 0:
					poke_radar = check_for_radar.first()
					poke_radar.add_charge(1)

				return redirect(profile_page, username)
		else:
			return redirect(user_not_found)
	else:
		return redirect(must_be_logged_in)

def view_adopt(request, pk, status="pokemon"):
	action = "Viewing a Pok&eacute;mon summary"
	update_online(request, action)

	adopt = Adopt.objects.filter(pk=pk)
	if adopt.count() is not 0:
		adopt = adopt.first()
		if request.user.is_authenticated():
			if request.user.username == adopt.owner.username:
				boxes = Box.objects.filter(user=request.user)

				evo_item = adopt.pokemon.evo_item
				if evo_item is not None:
					item = Item.objects.filter(name=evo_item)
					has_item = Inventory.objects.filter(user=request.user, item=item).exists()
			else:
				boxes = None
				has_item = False
				evo_item = None
		else:
			boxes = None
			has_item = False
			evo_item = None

		check_interaction(request.user, adopt)
		inventory = Inventory.objects.filter(user=request.user)

		if adopt.pokemon.name == "Eevee":
			water_stone = Item.objects.filter(name="water stone")
			has_eevee_water = Inventory.objects.filter(user=request.user, item=water_stone).exists()
			thunder_stone = Item.objects.filter(name="thunder stone")
			has_eevee_thunder = Inventory.objects.filter(user=request.user, item=thunder_stone).exists()
			fire_stone = Item.objects.filter(name="fire stone")
			has_eevee_fire = Inventory.objects.filter(user=request.user, item=fire_stone).exists()
		else:
			has_eevee_water = False
			has_eevee_thunder = False
			has_eevee_fire = False

		return render(request, 'site/view_adopt.html', {'adopt':adopt, 'boxes':boxes, 'has_item':has_item, 'item':evo_item, 'status':status, 'inventory':inventory, 'has_eevee_water':has_eevee_water, 'has_eevee_thunder':has_eevee_thunder, 'has_eevee_fire':has_eevee_fire})
	else:
		return redirect(pokemon_not_found)

def hatch_egg(request, pk):
	if request.user.is_authenticated():
		action = "Hatching an egg"
		update_online(request, action)

		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() is not 0:
			adopt = adopt.first()
			if adopt.owner == request.user:
				dex = Dex.objects.filter(user=request.user)
				if dex.count() is not 0:
					dex = dex.first()
					dex_egg_entry = dex.eggs.filter(name=adopt.pokemon.name).exists()
					dex_pokemon_entry = dex.pokemon.filter(name=adopt.pokemon.name).exists()

					if not dex_egg_entry:
						dex.add_egg_entry(adopt.pokemon)
					if not dex_pokemon_entry:
						dex.add_pokemon_entry(adopt.pokemon)


					check_for_radar = Hunt.objects.filter(user=request.user)
					if check_for_radar.count() != 0:
						poke_radar = check_for_radar.first()
						if poke_radar.charge < 50:
							poke_radar.reset_radar()
							hunt_multiplier = 1
						else:
							poke_radar.remove_charge(50)
							if poke_radar.reset:
								poke_radar.turn_off_reset()
							if adopt.pokemon == poke_radar.pokemon:
								poke_radar.hatch()
								hunt_multiplier = poke_radar.hatched
							elif adopt.pokemon == poke_radar.second_pokemon:
								poke_radar.hatch_second()
								hunt_multiplier = poke_radar.second_hatched
							else:
								hunt_multiplier = 1
					else:
						hunt_multiplier = 1

					if hunt_multiplier == 0:
						hunt_multiplier = 1

					# select random traits for pokemon
					random_gender = random.randint(1,100)
					if random_gender <= adopt.pokemon.percent_male:
						gender = True
					else:
						gender = False

					if hunt_multiplier > 50:
						hunt_multiplier = 50

					time_threshold = timezone.now() - timedelta(hours=24)
					shiny_charm = ShinyCharm.objects.filter(user=request.user, start_time__gte=time_threshold)
					if shiny_charm.count() != 0:
						hunt_multiplier *= 2

					if check_yesterday_hatched():
						shiny_chance = round(500/hunt_multiplier)
					else:
						shiny_chance = round(1000/hunt_multiplier)

					random_shiny = random.randint(1, shiny_chance)
					if random_shiny == 1: # 1/1000 chance
						shiny = True
						if check_for_radar.count() != 0:
							poke_radar = check_for_radar.first()
							gold_batteries = Item.objects.filter(name="gold batteries")
							check_for_gold_batteries = Inventory.objects.filter(user=request.user, item=gold_batteries)
							if check_for_gold_batteries.count() == 0:
								poke_radar.reset_radar()
					else:
						shiny = False

					random_nature = random.randint(0, 15)
					natures = ['hardy', 'lonely', 'brave', 'adamant', 'naughty', 'bold', 'docile', 'relaxed', 'impish', 'lax', 'timid', 'hasty', 'serious', 'jolly', 'naive', 'modest', 'mild', 'quiet', 'bashful', 'rash', 'calm', 'gentle', 'sassy', 'careful', 'quirky']
					nature = natures[random_nature]

					adopt.hatch(gender, shiny, nature, request.user)
					return redirect(view_adopt, pk=adopt.pk, status="hatched")
				else:
					return redirect(pokedex_index)
			else:
				return redirect(cannot_access)
		else:
			return redirect(pokemon_not_found)
	else:
		return redirect(must_be_logged_in)

def evolve_by_level(request, pk):
	if request.user.is_authenticated():
		action = "Evolving a Pok&eacute;mon"
		update_online(request, action)

		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() is not 0:
			adopt = adopt.first()

			if adopt.owner == request.user:
				if adopt.pokemon.evo:
					if adopt.total_exp == adopt.exp:
						evolution = Pokemon.objects.get(number=adopt.pokemon.evo)
						adopt.evolve(evolution, request.user)

						total_exp = 0
						multiplier = 1
						if adopt.pokemon.evo_level is not None:
							total_exp = adopt.pokemon.evo_level*1000
							multiplier = 1
							if adopt.pokemon.rate == "slow":
								multiplier = 2
							elif adopt.pokemon.rate == "medium slow":
								multiplier = 1.5
							elif adopt.pokemon.rate == "medium fast":
								multiplier = 1
							elif adopt.pokemon.rate == "fast":
								multiplier = .7

						total_exp*=multiplier
						adopt.total_exp = total_exp
						adopt.save()

						dex = Dex.objects.filter(user=request.user)
						if dex.count() is not 0:
							dex = dex.first()
							dex_pokemon_entry = dex.pokemon.filter(name=evolution.pokemon.name).exists()
							if not dex_pokemon_entry:
								dex.add_pokemon_entry(evolution)

							return redirect(view_adopt, pk=pk, status="evolved")

						else:
							return redirect(pokedex_index)
					else:
						return redirect(view_adopt, pk=pk, status="pokemon")
				else:
					return redirect(cannot_access)
			else:
				return redirect(pokemon_not_found)
		else:
			return redirect(pokemon_not_found)
	else:
		return redirect(must_be_logged_in)

def evolve_by_item(request, pk):
	if request.user.is_authenticated():
		action = "Evolving a Pok&eacute;mon"
		update_online(request, action)

		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() is not 0:
			adopt = adopt.first()

			if adopt.owner == request.user:
				if adopt.pokemon.evo:
					evo_item = adopt.pokemon.evo_item
					if evo_item is not None:
						item = Item.objects.filter(name=evo_item)
						has_item = Inventory.objects.filter(user=request.user, item=item)

						if has_item.count() != 0:
							item = has_item.first()
							if item.quantity > 1:
								item.quantity -= 1
								item.save()
							else:
								item.delete()

							evolution = Pokemon.objects.get(number=adopt.pokemon.evo)
							adopt.evolve(evolution, request.user)

							dex = Dex.objects.filter(user=request.user)
							if dex.count() is not 0:
								dex = dex.first()
								dex_pokemon_entry = dex.pokemon.filter(name=evolution.pokemon.name).exists()
								if not dex_pokemon_entry:
									dex.add_pokemon_entry(evolution)

								return redirect(view_adopt, pk=pk, status="evolved")
							else:
								return redirect(pokedex_index)
					else:
						return redirect(view_adopt, pk=pk)
				else:
					return redirect(cannot_access)
			else:
				return redirect(pokemon_not_found)
		else:
			return redirect(pokemon_not_found)
	else:
		return redirect(must_be_logged_in)

def evolve_eevee(request, pk, item):
	if request.user.is_authenticated():
		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() is not 0:
			adopt = adopt.first()
			if adopt.owner == request.user:
				if item == "water":
					item = Item.objects.filter(name="water stone")
					has_item = Inventory.objects.filter(user=request.user, item=item)
					evo_number = 134
				elif item == "thunder":
					item = Item.objects.filter(name="thunder stone")
					has_item = Inventory.objects.filter(user=request.user, item=item)
					evo_number = 135
				elif item == "fire":
					item = Item.objects.filter(name="fire stone")
					has_item = Inventory.objects.filter(user=request.user, item=item)
					evo_number = 136
				else:
					return redirect(view_adopt, pk=pk)

				if has_item.count() != 0:
					has_item = has_item.first()
					if has_item.quantity > 1:
						has_item.quantity -= 1
						has_item.save()
					else:
						has_item.delete()

					evolution = Pokemon.objects.get(number=evo_number)
					adopt.evolve(evolution, request.user)

					dex = Dex.objects.filter(user=request.user)
					if dex.count() is not 0:
						dex = dex.first()
						dex_pokemon_entry = dex.pokemon.filter(name=evolution.pokemon.name).exists()
						if not dex_pokemon_entry:
							dex.add_pokemon_entry(evolution)

						return redirect(view_adopt, pk=pk, status="evolved")
					else:
						return redirect(pokedex_index)


				else:
					return redirect(view_adopt, pk=pk)
			else:
				return redirect(cannot_access)
		else:
			return redirect(pokemon_not_found)
	else:
		return redirect(must_be_logged_in)


def evolve_by_trade(request, pk):
	if request.user.is_authenticated():
		action = "Evolving a Pok&eacute;mon"
		update_online(request, action)

		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() is not 0:
			adopt = adopt.first()

			if adopt.owner == request.user:
				if adopt.pokemon.evo:
					evolution = Pokemon.objects.get(number=adopt.pokemon.evo)
					adopt.evolve(evolution, request.user)

					dex = Dex.objects.filter(user=request.user)
					if dex.count() is not 0:
						dex = dex.first()
						dex_pokemon_entry = dex.pokemon.filter(name=evolution.pokemon.name).exists()
						if not dex_pokemon_entry:
							dex.add_pokemon_entry(evolution)

						return redirect(view_adopt, pk=pk, status="evolved")

					else:
						return redirect(pokedex_index)
				else:
					return redirect(pokemon_not_found)
			else:
				return redirect(cannot_access)
		else:
			return redirect(pokemon_not_found)
	else:
		return redirect(must_be_logged_in)

def change_nickname(request, pk):	
	if request.user.is_authenticated():
		action = "Changing a Pok&eacute;mon's nickname"
		update_online(request, action)

		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() is not 0:
			adopt = adopt.first()
			if request.user.username == adopt.owner.username:
				nickname = request.POST.get('nickname')
				adopt.change_nickname(nickname)
				return redirect(view_adopt, pk=pk, status='pokemon')
			else:
				return redirect(cannot_access)
		else:
			return redirect(pokemon_not_found)
	else:
		return redirect(must_be_logged_in)

def give_held_item(request, adopt_pk):
	if request.user.is_authenticated():
		action = "Giving a Pok&eacute;mon a held item"
		update_online(request, action)

		adopt = Adopt.objects.filter(pk=adopt_pk)
		if adopt.count() != 0:
			adopt = adopt.first()
			if adopt.owner == request.user:
				item_pk = request.POST.get("item_pk")
				item = Item.objects.filter(pk=item_pk).first()
				inventory = Inventory.objects.filter(user=request.user, item=item)
				if inventory.count() != 0:
					inventory = inventory.first()
					if inventory.quantity > 1:
						inventory.quantity -= 1
						inventory.save()
					else:
						inventory.delete()
					adopt.held_item = item
					adopt.save()
					return redirect(view_adopt, pk=adopt_pk, status='pokemon')
				else:
					return redirect(view_adopt, pk=adopt_pk, status='pokemon')
			else:
				return redirect(cannot_access)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def take_held_item(request, adopt_pk):
	if request.user.is_authenticated():
		adopt = Adopt.objects.filter(pk=adopt_pk)
		if adopt.count() != 0:
			adopt = adopt.first()
			if adopt.owner == request.user:
				if adopt.held_item is not None:
					item = Item.objects.filter(pk=adopt.held_item.pk).first()
					inventory = Inventory.objects.filter(item=item, user=request.user)
					if inventory.count() != 0:
						inventory = inventory.first()
						inventory.quantity += 1
						inventory.save()
					else:
						inventory = Inventory.objects.create(user=request.user, item=item)
					adopt.held_item = None
					adopt.save()
					return redirect(view_adopt, pk=adopt_pk, status='pokemon')
				else:
					return redirect(view_adopt, pk=adopt_pk, status='pokemon')
			else:
				return redirect(cannot_access)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)


# BOXES VIEWS

def boxes(request):
	if request.user.is_authenticated():
		action = "Viewing boxes"
		update_online(request, action)

		boxes = Box.objects.filter(user=request.user)
		if boxes.count() is not 0:

			voucher = Item.objects.filter(name="box voucher")
			check_for_vouchers = Inventory.objects.filter(item=voucher)
			if check_for_vouchers.count() != 0:
				return render(request, 'site/boxes.html', {'boxes':boxes, 'voucher':True})
			else:
				return render(request, 'site/boxes.html', {'boxes':boxes})
		else:
			return render(request, 'site/no_boxes.html')
	else:
		return render(request, 'site/unauthorized/boxes.html')

def create_box_page(request):
	if request.user.is_authenticated():

		box_list = Box.objects.filter(user=request.user)
		if box_list.count() == 0:
			action = "Creating a box"
			update_online(request, action)

			return render(request, 'site/create_box.html', {'first':True})
		else:
			voucher = Item.objects.filter(name="box voucher")
			check_for_vouchers = Inventory.objects.filter(item=voucher)
			if check_for_vouchers.count() != 0:
				action = "Creating a box"
				update_online(request, action)
				return render(request, 'site/create_box.html', {'voucher':True})
			else:
				return redirect(boxes)
	else:
		return redirect(must_be_logged_in)

def create_box(request):
	if request.user.is_authenticated():
		user = request.user
		box_name = request.POST.get("name")
		wallpaper = request.POST.get("wallpaper")

		box_list = Box.objects.filter(user=request.user)
		if box_list.count() == 0:
			box = Box.objects.create(user=user, name=box_name, wallpaper=wallpaper)
			return redirect(boxes)
		else:
			voucher = Item.objects.filter(name="box voucher")
			check_for_vouchers = Inventory.objects.filter(item=voucher)
			if check_for_vouchers.count() != 0:
				voucher = check_for_vouchers.first()
				if voucher.quantity > 1:
					voucher.quantity -= 1
					voucher.save()
				else:
					voucher.delete()
				box = Box.objects.create(user=user, name=box_name, wallpaper=wallpaper)
				return redirect(boxes)
			else:
				return redirect(boxes)
	else:
		return redirect(must_be_logged_in)

def edit_box(request, pk):
	if request.user.is_authenticated():
		box_name = request.POST.get("name")
		wallpaper = request.POST.get("wallpaper")

		box = Box.objects.filter(pk=pk)
		if box.count() != 0:
			box = box.first()
			box.name = box_name
			if wallpaper is None:
				box.wallpaper = box.wallpaper
			else:
				box.wallpaper = wallpaper
			box.save()

		return redirect(boxes)
	else:
		return redirect(must_be_logged_in)

def delete_box(request, pk):
	if request.user.is_authenticated():
		box = Box.objects.filter(pk=pk)
		if box.count() != 0:
			box = box.first()

			pokemon_in_box = False
			for pokemon in box.pokemon.all():
				pokemon_in_box = True

			if pokemon_in_box:
				return redirect(boxes)
			else:
				box.delete()
				return redirect(boxes)
		else:
			return redirect(boxes)
	else:
		return redirect(must_be_logged_in)


def move_to_box(request, box, adopt):
	if request.user.is_authenticated():
		adopt = Adopt.objects.filter(pk=adopt)
		if adopt.count() is 0:
			return redirect(pokemon_not_found)
		else:
			adopt = adopt.first()
			if adopt.owner.username == request.user.username:
				if adopt.party:
					box_list = Box.objects.filter(pk=box)
					if box_list.count() is 0:
						return redirect(boxes)
					else:
						box = box_list.first()
						if box.pokemon.count() < 25:
							adopt.from_party_to_box()
							box.add_pokemon(adopt)
							return redirect(boxes)
						else:
							return redirect(profile_page, request.user.username)
				else:
					return redirect(profile_page, username=request.user.username)
			else: 
				return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)


def move_to_different_box(request, box, adopt):
	if request.user.is_authenticated():
		adopt = Adopt.objects.filter(pk=adopt)
		if adopt.count() is 0:
			return redirect(pokemon_not_found)
		else:
			adopt = adopt.first()
			if adopt.owner.username == request.user.username:
				box_list = Box.objects.filter(pk=box)
				if box_list.count() is 0:
					return redirect(boxes)
				else:
					box = box_list.first()

					if box.pokemon.count() < 25:
						box_list = Box.objects.filter(user=request.user)
						any_box_pk = 1000000
						for each_box in box_list:
							if each_box.pokemon.filter(pk=adopt.pk).exists():
								each_box.remove_pokemon(adopt)
								any_box_pk = each_box.pk
						if box.pk != any_box_pk:
							adopt.box_time = timezone.now()
							adopt.save()
							box.add_pokemon(adopt)
						return redirect(boxes)
					else:
						return redirect(profile_page, request.user.username)
			else: 
				return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def move_to_party(request, adopt):
	if request.user.is_authenticated():
		adopt = Adopt.objects.filter(pk=adopt)
		if adopt.count() is 0:
			return redirect(pokemon_not_found)
		else:
			adopt = adopt.first()
			if adopt.owner.username == request.user.username:

				amount_in_party = Adopt.objects.filter(owner=request.user, party=True, daycare=False, gts=False).count()
				if amount_in_party < 6:
					adopt.from_box_to_party()
					box_list = Box.objects.filter(user=request.user)
					for box in box_list:
						if box.pokemon.filter(pk=adopt.pk).exists():
							box.remove_pokemon(adopt)
					return redirect(profile_page, request.user.username)
				else:
					return redirect(boxes)

			else: 
				return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)


# POKEDEX VIEWS 

def pokedex_index(request):
	if request.user.is_authenticated():
		check_for_dex = Dex.objects.filter(user=request.user)
		if check_for_dex.count() != 0:
			action = "Viewing the Pok&eacute;dex"
			update_online(request, action)

			pokemon = Pokemon.objects.all()
			dex = check_for_dex.first()

			for monster in pokemon:
				monster.percent_female = 100 - monster.percent_male
				monster.egg_dex_entered = dex.eggs.filter(name=monster.name).exists()
				monster.pokedex_entered = dex.pokemon.filter(name=monster.name).exists()

			return render(request, 'pokedex/index.html', {'pokemon':pokemon})
		else:
			return render(request, 'pokedex/no_dex.html')
	else:
		return render(request, 'pokedex/unauthorized/pokedex.html')

def receive_pokedex(request):
	if request.user.is_authenticated():
		check_for_dex = Dex.objects.filter(user=request.user)
		if check_for_dex.count() == 0:
			dex = Dex.objects.create(user=request.user)
			return redirect(lab)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

# INVENTORY VIEWS

def inventory(request):
	if request.user.is_authenticated():
		bag = Item.objects.filter(name="bag").first()
		check_for_inventory = Inventory.objects.filter(user=request.user, item=bag)
		if check_for_inventory.count() != 0:
			action = "Viewing Inventory"
			update_online(request, action)

			inventory = Inventory.objects.filter(user=request.user)

			return render(request, 'site/inventory.html', {'inventory':inventory})
		else:
			return render(request, 'site/no_inventory.html')
	else:
		return redirect(must_be_logged_in)

def sell_item(request, item_pk):
	if request.user.is_authenticated():
		item = Item.objects.filter(pk=item_pk)
		sell_quantity = int(request.POST.get('quantity'))
		check_for_inventory = Inventory.objects.filter(user=request.user, item=item)
		if check_for_inventory.count() == 0:
			# does not have any
			# return redirect(inventory)
			raise ValueError("Doesnt have any")
		else:
			item = check_for_inventory.first()
			if item.quantity < sell_quantity:
				# trying to sell more than owns
				# return redirect(inventory)
				raise ValueError("Trying to sell more than own")
			else:
				# selling is possible
				value = sell_quantity * item.item.sell_value
				currency = Currency.objects.filter(user=request.user)
				currency = currency.first()

				currency.get_pd(value)
				if (item.quantity - sell_quantity) == 0:
					item.delete()
					return redirect(inventory)
					# raise ValueError("Deleted, should work")
				else:
					new_quantity = item.quantity - sell_quantity
					item.change_quantity(new_quantity)
					return redirect(inventory)
					# raise ValueError("Change quantity, should work")

	else:
		return redirect(must_be_logged_in)

def parcel_page(request):
	if request.user.is_authenticated():
		action = "Viewing parcels"
		update_online(request, action)

		parcel = Item.objects.filter(name="parcel").first()
		has_parcel = Inventory.objects.filter(item=parcel).first()
		parcel_quantity = ""
		if has_parcel is not None:
			for i in range(0, has_parcel.quantity):
				parcel_quantity += "x"

		parcel_parcel = Item.objects.filter(name="parcel parcel").first()
		has_parcel_parcel = Inventory.objects.filter(item=parcel_parcel).first()
		parcel_parcel_quantity = ""
		if has_parcel_parcel is not None:
			for i in range(0, has_parcel_parcel.quantity):
				parcel_parcel_quantity += "x"

		return render(request, 'site/parcel.html', {'parcel':parcel, 'has_parcel':has_parcel, 'parcel_quantity':parcel_quantity, 'parcel_parcel':parcel_parcel, 'has_parcel_parcel':has_parcel_parcel, 'parcel_parcel_quantity':parcel_parcel_quantity, })
	else:
		return redirect(must_be_logged_in)

def open_parcel(request):
	if request.user.is_authenticated():
		parcel = Item.objects.filter(name="parcel").first()
		parcel = Inventory.objects.filter(user=request.user, item=parcel)
		if parcel.count() != 0:
			parcel = parcel.first()
			if parcel.quantity > 1:
				parcel.quantity -= 1
				parcel.save()
			else:
				parcel.delete()

			random_item = random.randint(1, 15)
			if random_item <= 8:
				# berry
				random_berry = random.randint(0, 4)
				berries = ["aguav berry", "leppa berry", "chesto berry", "kasib berry", "sitrus berry"]
				berry = Item.objects.filter(name=berries[random_berry]).first()
				has_berry = Inventory.objects.filter(user=request.user, item=berry)
				random_berry_quantity = random.randint(1, 5)
				if has_berry.count() != 0:
					berry = has_berry.first()
					berry.quantity += random_berry_quantity
					berry.save()
				else:
					berry = Inventory.objects.create(user=request.user, item=berry, quantity=random_berry_quantity)
				message = str(random_berry_quantity) + " " + berries[random_berry]
			elif random_item <= 12:
				# PD < 1500
				currency = Currency.objects.get(user=request.user)
				pd_amount = random.randint(100, 1500)
				currency.get_pd(pd_amount)
				message = str(pd_amount) + " PD"
			elif random_item <= 14:
				# evolution item
				random_stone = random.randint(0, 4)
				stones = ["fire stone", "moon stone", "water stone", "thunder stone", "leaf stone"]
				stone = Item.objects.filter(name=stones[random_stone]).first()
				has_stone = Inventory.objects.filter(user=request.user, item=stone)
				if has_stone.count() != 0:
					stone = has_stone.first()
					stone.quantity += 1
					stone.save()
				else:
					stone = Inventory.objects.create(user=request.user, item=stone)
				message = stones[random_stone]
			else:
				# coins
				currency = Currency.objects.get(user=request.user)
				coins_amount = random.randint(5, 20)
				currency.get_coins(coins_amount)
				message = str(coins_amount) + " Coins"


			parcel = Item.objects.filter(name="parcel").first()
			has_parcel = Inventory.objects.filter(user=request.user, item=parcel).first()
			parcel_quantity = ""
			if has_parcel is not None:
				for i in range(0, has_parcel.quantity):
					parcel_quantity += "x"

			gold_parcel = Item.objects.filter(name="gold parcel").first()
			has_gold_parcel = Inventory.objects.filter(user=request.user, item=gold_parcel).first()
			gold_parcel_quantity = ""
			if has_gold_parcel is not None:
				for i in range(0, has_gold_parcel.quantity):
					gold_parcel_quantity += "x"

			parcel_parcel = Item.objects.filter(name="parcel parcel").first()
			has_parcel_parcel = Inventory.objects.filter(user=request.user, item=parcel_parcel).first()
			parcel_parcel_quantity = ""
			if has_parcel_parcel is not None:
				for i in range(0, has_parcel_parcel.quantity):
					parcel_parcel_quantity += "x"

			return render(request, 'site/parcel_opened.html', {'message':message, 'parcel':parcel, 'has_parcel':has_parcel, 'parcel_quantity':parcel_quantity, 'parcel_parcel':parcel_parcel, 'has_parcel_parcel':has_parcel_parcel, 'parcel_parcel_quantity':parcel_parcel_quantity,  'gold_parcel_quantity':gold_parcel_quantity, 'gold_parcel':gold_parcel, 'has_gold_parcel':has_gold_parcel})

		else:
			return redirect(parcel_page)
	else:
		return redirect(must_be_logged_in)

def open_parcel_parcel(request):
	if request.user.is_authenticated():
		parcel_item = Item.objects.filter(name="parcel").first()
		parcel = Inventory.objects.filter(user=request.user, item=parcel_item)

		parcel_parcel = Item.objects.filter(name="parcel parcel").first()
		parcel_parcel = Inventory.objects.filter(user=request.user, item=parcel_parcel)

		if parcel_parcel.count() != 0:
			parcel_parcel = parcel_parcel.first()
			if parcel_parcel.quantity > 1:
				parcel_parcel.quantity -= 1
				parcel_parcel.save()
			else:
				parcel_parcel.delete()

			if parcel.count() != 0:
				parcel = parcel.first()
				if parcel.quantity > 1:
					parcel.quantity += 10
					parcel.save()
				else:
					parcel = Inventory.objects.create(item=parcel_item, user=request.user, quantity=10)
			return redirect(parcel_page)
		else:
			return redirect(parcel_page)
	else:
		return redirect(must_be_logged_in)

# POKEMART VIEWS

def pokemart(request):
	if request.user.is_authenticated():
		action = "Visiting the Pok&eacute;mart"
		update_online(request, action)

		bag = Item.objects.filter(name="bag").first()
		check_for_inventory = Inventory.objects.filter(user=request.user, item=bag)
		if check_for_inventory.count() == 0:
			return render(request, 'site/pokemart_new_user.html')
		else:
			items = Item.objects.all()
			if check_yesterday_berry_interactions():
				for item in items:
					item.purchase_value = int(item.purchase_value*0.75)
			return render(request, 'site/pokemart.html', {'items':items, 'sale':check_yesterday_berry_interactions()})
	else:
		return render(request, 'site/unauthorized/pokemart.html')

def receive_bag(request):
	if request.user.is_authenticated():
		bag = Item.objects.filter(name="bag").first()
		check_for_inventory = Inventory.objects.filter(user=request.user, item=bag)
		if check_for_inventory.count() == 0:
			new_bag = Inventory.objects.create(user=request.user, item=bag)
			return redirect(inventory)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def purchase_item(request, item_pk):
	if request.user.is_authenticated():
		next = request.POST.get('next', '/')
		item = Item.objects.filter(pk=item_pk).first()
		purchase_quantity = int(request.POST.get('quantity'))

		value = purchase_quantity * item.purchase_value
		if check_yesterday_berry_interactions():
			value = value*0.75

		currency = Currency.objects.filter(user=request.user)
		currency = currency.first()
		if value > currency.pd:
			# can't afford
			return HttpResponseRedirect(next)
		else:
			# check inventory so that if you already have some, it just changes the quantity
			check_for_inventory = Inventory.objects.filter(user=request.user, item=item)
			currency.spend_pd(value)
			if check_for_inventory.count() == 0:
				# doesnt have any
				inventory = Inventory.objects.create(user=request.user, item=item, quantity=purchase_quantity)	
				return HttpResponseRedirect(next)
			else:
				# has some already
				inventory = check_for_inventory.first()
				new_quantity = inventory.quantity + purchase_quantity
				inventory.change_quantity(new_quantity)
				return HttpResponseRedirect(next)
	else:
		return redirect(must_be_logged_in)

def purchase_gold_item(request, item_pk):
	if request.user.is_authenticated():
		next = request.POST.get('next', '/')
		item = Item.objects.filter(pk=item_pk).first()
		purchase_quantity = int(request.POST.get('quantity'))

		value = purchase_quantity * item.purchase_value_coins
		if check_yesterday_berry_interactions():
			value = value*0.75

		currency = Currency.objects.filter(user=request.user)
		currency = currency.first()
		if value > currency.coins:
			# can't afford
			return HttpResponseRedirect(next)
		else:
			# check inventory so that if you already have some, it just changes the quantity
			check_for_inventory = Inventory.objects.filter(user=request.user, item=item)
			currency.spend_coins(value)
			if check_for_inventory.count() == 0:
				# doesnt have any
				inventory = Inventory.objects.create(user=request.user, item=item, quantity=purchase_quantity)
				return HttpResponseRedirect(next)
			else:
				# has some already
				inventory = check_for_inventory.first()
				new_quantity = inventory.quantity + purchase_quantity
				inventory.change_quantity(new_quantity)
				return HttpResponseRedirect(next)
	else:
		return redirect(must_be_logged_in)

# PARK VIEWS

def park(request):
	if request.user.is_authenticated():
		action = "Visiting the Park"
		update_online(request, action)

		incense = Item.objects.get(name="incense")
		has_incense = Inventory.objects.filter(user=request.user, item=incense)

		repel = Item.objects.get(name="repel")
		has_repel = Inventory.objects.filter(user=request.user, item=repel)

		if has_incense.count() != 0:
			has_incense = True
		else:
			has_incense = False

		if has_repel.count() != 0:
			has_repel = True
		else:
			has_repel = False

		cedar = User.objects.filter(username="CEDAR")
		park_pokemon = Adopt.objects.filter(owner=cedar).order_by('?')[:10]
		for pokemon in park_pokemon:
			pokemon.x_percent = random.randint(0, 100)
			pokemon.y_percent = random.randint(0, 100)

		park_passes = Item.objects.filter(category="park pass")

		basic_park_pass = Item.objects.get(name="basic park pass")
		has_basic_park_pass = Inventory.objects.filter(user=request.user, item=basic_park_pass)
		if has_basic_park_pass.count() != 0:

			today = dt_datetime.now().date()
			park_adopts_today = Adopt.objects.filter(owner=request.user, park_adopt=True, update_time__gte=today).count()

			bronze_park_pass = Item.objects.get(name="bronze park pass")
			has_bronze_park_pass = Inventory.objects.filter(user=request.user, item=bronze_park_pass)
			if has_bronze_park_pass.count() != 0:
				has_bronze_park_pass = True
			else:
				has_bronze_park_pass = False

			silver_park_pass = Item.objects.get(name="silver park pass")
			has_silver_park_pass = Inventory.objects.filter(user=request.user, item=silver_park_pass)
			if has_silver_park_pass.count() != 0:
				has_silver_park_pass = True
			else:
				has_silver_park_pass = False

			gold_park_pass = Item.objects.get(name="gold park pass")
			has_gold_park_pass = Inventory.objects.filter(user=request.user, item=gold_park_pass)
			if has_gold_park_pass.count() != 0:
				has_gold_park_pass = True
			else:
				has_gold_park_pass = False

			park_items = Item.objects.filter(category="park item").order_by('purchase_value_coins')

			return render(request, 'site/park.html', {'park_pokemon':park_pokemon, 'park_passes':park_passes, 'park_adopts_today':park_adopts_today, 'has_bronze_park_pass':has_bronze_park_pass, 'has_silver_park_pass':has_silver_park_pass, 'has_gold_park_pass':has_gold_park_pass, 'park_items':park_items, 'has_incense':has_incense, 'has_repel':has_repel})
		else:
			return render(request, 'site/park_new_user.html')

	else:
		return render(request, 'site/unauthorized/park.html')

def park_incense(request):
	if request.user.is_authenticated():
		action = "Visiting the Park"
		update_online(request, action)

		incense = Item.objects.get(name="incense")
		has_incense = Inventory.objects.filter(user=request.user, item=incense)
		repel = Item.objects.get(name="repel")
		has_repel = Inventory.objects.filter(user=request.user, item=repel)

		if has_incense.count() != 0:
			has_incense = True
			if has_repel.count() != 0:
				has_repel = True
			else:
				has_repel = False

			cedar = User.objects.filter(username="CEDAR")
			park_pokemon = Adopt.objects.filter(owner=cedar, hatched=True).order_by('?')[:10]
			for pokemon in park_pokemon:
				pokemon.x_percent = random.randint(0, 100)
				pokemon.y_percent = random.randint(0, 100)

			park_passes = Item.objects.filter(category="park pass")

			basic_park_pass = Item.objects.get(name="basic park pass")
			has_basic_park_pass = Inventory.objects.filter(user=request.user, item=basic_park_pass)
			if has_basic_park_pass.count() != 0:

				today = dt_datetime.now().date()
				park_adopts_today = Adopt.objects.filter(owner=request.user, park_adopt=True, update_time__gte=today).count()

				bronze_park_pass = Item.objects.get(name="bronze park pass")
				has_bronze_park_pass = Inventory.objects.filter(user=request.user, item=bronze_park_pass)
				if has_bronze_park_pass.count() != 0:
					has_bronze_park_pass = True
				else:
					has_bronze_park_pass = False

				silver_park_pass = Item.objects.get(name="silver park pass")
				has_silver_park_pass = Inventory.objects.filter(user=request.user, item=silver_park_pass)
				if has_silver_park_pass.count() != 0:
					has_silver_park_pass = True
				else:
					has_silver_park_pass = False

				gold_park_pass = Item.objects.get(name="gold park pass")
				has_gold_park_pass = Inventory.objects.filter(user=request.user, item=gold_park_pass)
				if has_gold_park_pass.count() != 0:
					has_gold_park_pass = True
				else:
					has_gold_park_pass = False

				park_items = Item.objects.filter(category="park item").order_by('purchase_value_coins')

				return render(request, 'site/park.html', {'park_pokemon':park_pokemon, 'park_passes':park_passes, 'park_adopts_today':park_adopts_today, 'has_bronze_park_pass':has_bronze_park_pass, 'has_silver_park_pass':has_silver_park_pass, 'has_gold_park_pass':has_gold_park_pass, 'park_items':park_items, 'has_incense':has_incense, 'has_repel':has_repel})
	
			else:
				return render(request, 'site/park_new_user.html')
		else:
			return redirect(park)
	else:
		return render(request, 'site/unauthorized/park.html')

def park_repel(request):
	if request.user.is_authenticated():
		action = "Visiting the Park"
		update_online(request, action)

		repel = Item.objects.get(name="repel")
		has_repel = Inventory.objects.filter(user=request.user, item=repel)
		incense = Item.objects.get(name="incense")
		has_incense = Inventory.objects.filter(user=request.user, item=incense)

		if has_repel.count() != 0:
			has_repel = True
			if has_incense.count() != 0:
				has_incense = True
			else:
				has_incense = False

			cedar = User.objects.filter(username="CEDAR")
			park_pokemon = Adopt.objects.filter(owner=cedar, hatched=False).order_by('?')[:10]
			for pokemon in park_pokemon:
				pokemon.x_percent = random.randint(0, 100)
				pokemon.y_percent = random.randint(0, 100)

			park_passes = Item.objects.filter(category="park pass")

			basic_park_pass = Item.objects.get(name="basic park pass")
			has_basic_park_pass = Inventory.objects.filter(user=request.user, item=basic_park_pass)
			if has_basic_park_pass.count() != 0:

				today = dt_datetime.now().date()
				park_adopts_today = Adopt.objects.filter(owner=request.user, park_adopt=True, update_time__gte=today).count()

				bronze_park_pass = Item.objects.get(name="bronze park pass")
				has_bronze_park_pass = Inventory.objects.filter(user=request.user, item=bronze_park_pass)
				if has_bronze_park_pass.count() != 0:
					has_bronze_park_pass = True
				else:
					has_bronze_park_pass = False

				silver_park_pass = Item.objects.get(name="silver park pass")
				has_silver_park_pass = Inventory.objects.filter(user=request.user, item=silver_park_pass)
				if has_silver_park_pass.count() != 0:
					has_silver_park_pass = True
				else:
					has_silver_park_pass = False

				gold_park_pass = Item.objects.get(name="gold park pass")
				has_gold_park_pass = Inventory.objects.filter(user=request.user, item=gold_park_pass)
				if has_gold_park_pass.count() != 0:
					has_gold_park_pass = True
				else:
					has_gold_park_pass = False

				park_items = Item.objects.filter(category="park item").order_by('purchase_value_coins')

				return render(request, 'site/park.html', {'park_pokemon':park_pokemon, 'park_passes':park_passes, 'park_adopts_today':park_adopts_today, 'has_bronze_park_pass':has_bronze_park_pass, 'has_silver_park_pass':has_silver_park_pass, 'has_gold_park_pass':has_gold_park_pass, 'park_items':park_items, 'has_incense':has_incense, 'has_repel':has_repel})
				
			else:
				return render(request, 'site/park_new_user.html')
		else:
			return redirect(park)
	else:
		return render(request, 'site/unauthorized/park.html')

def receive_park_pass(request):
	if request.user.is_authenticated():
		park_pass = Item.objects.get(name="basic park pass")
		check_for_park_pass = Inventory.objects.filter(user=request.user, item=park_pass)
		if check_for_park_pass.count() == 0:
			park_pass = Inventory.objects.create(user=request.user, item=park_pass)
			return redirect(park)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def park_adopt(request, pk):
	if request.user.is_authenticated():
		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() is not 0:
			adopt = adopt.first()

			check_for_dex = Dex.objects.filter(user=request.user)
			if check_for_dex.count() != 0:

				amount_in_party = Adopt.objects.filter(owner=request.user, party=True).count()
				if amount_in_party < 6:
					if adopt.owner.username == "CEDAR":

						today = dt_datetime.now().date()
						park_adopts_today = Adopt.objects.filter(owner=request.user, park_adopt=True, update_time__gte=today).count()
						
						bronze_park_pass = Item.objects.get(name="bronze park pass")
						has_bronze_park_pass = Inventory.objects.filter(user=request.user, item=bronze_park_pass)
						if has_bronze_park_pass.count() != 0:
							has_bronze_park_pass = True
						else:
							has_bronze_park_pass = False

						silver_park_pass = Item.objects.get(name="silver park pass")
						has_silver_park_pass = Inventory.objects.filter(user=request.user, item=silver_park_pass)
						if has_silver_park_pass.count() != 0:
							has_silver_park_pass = True
						else:
							has_silver_park_pass = False

						gold_park_pass = Item.objects.get(name="gold park pass")
						has_gold_park_pass = Inventory.objects.filter(user=request.user, item=gold_park_pass)
						if has_gold_park_pass.count() != 0:
							has_gold_park_pass = True
						else:
							has_gold_park_pass = False

						can_adopt = False
						if park_adopts_today < 3:
							can_adopt = True
						elif park_adopts_today >= 3:
							if has_gold_park_pass:
								if park_adopts_today < 24:
									can_adopt = True
								else:
									can_adopt = False
							elif has_silver_park_pass:
								if park_adopts_today < 12:
									can_adopt = True
								else:
									can_adopt = False
							elif has_bronze_park_pass:
								if park_adopts_today < 6:
									can_adopt = True
								else:
									can_adopt = False
							else:
								can_adopt = False

						if can_adopt:
							adopt.park_adopt = True
							adopt.save()
							adopt.change_owner(request.user)
							return redirect(park)
						else:
							return redirect(park)
					else:
						return redirect(cannot_access)
				else:
					return redirect(party_is_full)
			else:
				return redirect(pokedex_index)
		else:
			return redirect(pokemon_not_found)
	else:
		return redirect(must_be_logged_in)

def release_adopt(request, pk):
	if request.user.is_authenticated():
		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() is not 0:
			adopt = adopt.first()
			if request.user.username == adopt.owner.username:
				time_threshold = timezone.now() - timedelta(hours=2)	
				if adopt.update_time <= time_threshold:

					if not adopt.party:
						box_list = Box.objects.filter(user=request.user)
						for box in box_list:
							if box.pokemon.filter(pk=adopt.pk).exists():
								box.remove_pokemon(adopt)
					cedar = User.objects.get(username="CEDAR")
					adopt.change_owner(cedar)
					return redirect(profile_page, username=request.user.username)
				else:
					return redirect(view_adopt, pk=pk, status='pokemon')
			else:
				return redirect(cannot_access)
		else:
			return redirect(pokemon_not_found)
	else:
		return redirect(must_be_logged_in)

# DAYCARE VIEWS

def daycare(request):
	if request.user.is_authenticated():
		action = "Visiting the Daycare"
		update_online(request, action)

		adopts_in_daycare = Adopt.objects.filter(owner=request.user, daycare=True).order_by('update_time')

		if adopts_in_daycare.count() == 2:
			if adopts_in_daycare[0].pokemon.number == adopts_in_daycare[1].pokemon.number:
				same_pokemon = True
			else:
				same_pokemon = False

			if adopts_in_daycare[0].gender == True and adopts_in_daycare[1].gender == False:
				opposite_genders = True
			elif adopts_in_daycare[0].gender == False and adopts_in_daycare[1].gender == True:
				opposite_genders = True
			else:
				opposite_genders = False
		else:
			same_pokemon = False
			opposite_genders = False

		poke_puffs = Item.objects.filter(category="poke puff")

		basic_poke_puff = Item.objects.get(name="basic poke puff")
		frosted_poke_puff = Item.objects.get(name="frosted poke puff")
		fancy_poke_puff = Item.objects.get(name="fancy poke puff")
		deluxe_poke_puff = Item.objects.get(name="deluxe poke puff")
		supreme_poke_puff = Item.objects.get(name="supreme poke puff")

		poke_puffs_in_inventory = Inventory.objects.filter(item=basic_poke_puff) | Inventory.objects.filter(item=frosted_poke_puff) | Inventory.objects.filter(item=fancy_poke_puff) | Inventory.objects.filter(item=deluxe_poke_puff) | Inventory.objects.filter(item=supreme_poke_puff)

		contract_license = Item.objects.filter(name="contract license")
		has_contract_license = Inventory.objects.filter(user=request.user, item=contract_license).exists()

		contract = Contract.objects.filter(user=request.user).first()
		potential_contract = PotentialContract.objects.filter(user=request.user).first()

		daycare_items = Item.objects.filter(category="daycare item")
		daycare_eggs = DaycareEgg.objects.filter(user=request.user)

		today = dt_datetime.now().date()
		daycare_adopts = Adopt.objects.filter(owner=request.user, daycare_adopt=True, update_time__gte=today).count()
		egg_permit = Item.objects.filter(name="egg permit")
		has_egg_permit = Inventory.objects.filter(user=request.user, item=egg_permit).exists()

		return render(request, 'site/daycare.html', {'adopts_in_daycare':adopts_in_daycare, 'same_pokemon':same_pokemon, 'opposite_genders':opposite_genders, 'poke_puffs':poke_puffs, 'poke_puffs_in_inventory':poke_puffs_in_inventory, 'contract':contract, 'potential_contract':potential_contract, 'has_contract_license':has_contract_license, 'daycare_items':daycare_items, 'daycare_eggs':daycare_eggs, 'daycare_adopts':daycare_adopts, 'has_egg_permit':has_egg_permit})
	else:
		return render(request, 'site/unauthorized/daycare.html')

def drop_off_adopt_page(request):
	if request.user.is_authenticated():
		adopts_in_party = Adopt.objects.filter(owner=request.user, hatched=True, party=True, gts=False, daycare=False)
		boxes = Box.objects.filter(user=request.user)
		return render(request, 'site/drop_off_adopt.html', {'boxes':boxes, 'adopts_in_party':adopts_in_party})
	else:
		return redirect(must_be_logged_in)

def drop_off_adopt(request):
	if request.user.is_authenticated():
		adopts_in_daycare = Adopt.objects.filter(owner=request.user, daycare=True)
		if adopts_in_daycare.count() < 2:
			adopt_pk = request.POST.get("adopt_pk")
			adopt = Adopt.objects.filter(pk=adopt_pk)
			if adopt.count() != 0:
				adopt = adopt.first()
				adopt.daycare = True
				adopt.save()
				adopt.from_box_to_party()
				box_list = Box.objects.filter(user=request.user)
				for box in box_list:
					if box.pokemon.filter(pk=adopt.pk).exists():
						box.remove_pokemon(adopt)
				return redirect(daycare)
			else:
				return redirect(daycare)
		else:
			return redirect(daycare)
	else:
		return redirect(must_be_logged_in)

def pick_up_adopt(request, pk):
	if request.user.is_authenticated():
		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() != 0:
			adopt = adopt.first()
			if request.user == adopt.owner:
				party_pokemon = Adopt.objects.filter(owner=request.user, party=True, gts=False, daycare=False)
				if party_pokemon.count() < 6:
					adopt.daycare = False
					adopt.save()
					return redirect(daycare)
				else:
					return redirect(party_is_full)
			else:
				return redirect(cannot_access)
		else:
			return redirect(daycare)
	else:
		return redirect(must_be_logged_in)

def adopt_daycare_egg(request, pk):
	if request.user.is_authenticated():
		daycare_egg = DaycareEgg.objects.filter(pk=pk)
		if daycare_egg.count() != 0:
			daycare_egg = daycare_egg.first()
			if daycare_egg.user == request.user:

				adopts_in_party = Adopt.objects.filter(owner=request.user, hatched=True, party=True, gts=False, daycare=False).count()
				if adopts_in_party < 6:

					today = dt_datetime.now().date()
					daycare_adopts = Adopt.objects.filter(owner=request.user, daycare_adopt=True, update_time__gte=today).count()
					
					egg_permit = Item.objects.filter(name="egg permit")
					has_egg_permit = Inventory.objects.filter(user=request.user, item=egg_permit).exists()

					can_adopt = False
					if daycare_adopts == 0:
						can_adopt = True
					elif daycare_adopts == 1 and has_egg_permit:
						can_adopt = True
					else:
						can_adopt = False

					if can_adopt:
						total_exp = 0
						multiplier = 1
						if daycare_egg.pokemon.evo_level is not None:
							total_exp = daycare_egg.pokemon.evo_level*1000
							multiplier = 1
							if daycare_egg.pokemon.rate == "slow":
								multiplier = 2
							elif daycare_egg.pokemon.rate == "medium slow":
								multiplier = 1.5
							elif daycare_egg.pokemon.rate == "medium fast":
								multiplier = 1
							elif daycare_egg.pokemon.rate == "fast":
								multiplier = .7

							total_exp*=multiplier


						adopt = Adopt.objects.create(owner=request.user, pokemon=daycare_egg.pokemon, hatched=False, exp=0, happiness=0, gender=True, total_exp=total_exp, daycare_adopt=True)
						daycare_egg.delete()
						return redirect(daycare)
					else:
						return redirect(party_is_full)
				else:
					return redirect(daycare)
			else:
				return redirect(cannot_access)
		else:
			return redirect(daycare)
	else:
		return redirect(must_be_logged_in)

def feed_poke_puff(request, adopt_pk):
	if request.user.is_authenticated():
		adopt = Adopt.objects.get(pk=adopt_pk)
		if adopt.owner == request.user and adopt.daycare:
			poke_puff_pk = request.POST.get("poke_puff_pk")
			poke_puff = Inventory.objects.filter(user=request.user, pk=poke_puff_pk)
			if poke_puff.count() != 0:
				poke_puff = poke_puff.first()

				if poke_puff.item.name == "basic poke puff":
					happiness_gain = 2
				elif poke_puff.item.name == "frosted poke puff":
					happiness_gain = 4
				elif poke_puff.item.name == "fancy poke puff":
					happiness_gain = 6
				elif poke_puff.item.name == "deluxe poke puff":
					happiness_gain = 10
				elif poke_puff.item.name == "supreme poke puff":
					happiness_gain = 20
				else:
					happiness_gain = 0

				adopt.happiness += happiness_gain
				adopt.save()

				if poke_puff.quantity > 1:
					poke_puff.quantity -= 1
					poke_puff.save()
				else:
					poke_puff.delete()

				return redirect(daycare)

			else:
				return redirect(daycare)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def create_potential_contract(request):
	if request.user.is_authenticated():
		contract_license = Item.objects.filter(name="contract license")
		has_contract_license = Inventory.objects.filter(user=request.user, item=contract_license).exists()
		if has_contract_license:

			contracts = Contract.objects.filter(user=request.user)
			potential_contracts = PotentialContract.objects.filter(user=request.user)

			if contracts.count() == 0 and potential_contracts.count() == 0:
				get_difficulty = random.randint(1, 31)
				if get_difficulty <= 16:
					difficulty = 1
				elif get_difficulty <= 24:
					difficulty = 2
				elif get_difficulty <= 28:
					difficulty = 3
				elif get_difficulty <= 30:
					difficulty = 4
				else:
					difficulty = 5

				potential_contract = PotentialContract.objects.create(user=request.user, difficulty=difficulty)
				return redirect(daycare)
			else:
				return redirect(daycare)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def accept_potential_contract(request):
	if request.user.is_authenticated():
		potential_contract = PotentialContract.objects.filter(user=request.user)
		if potential_contract.exists():
			potential_contract = potential_contract.first()
			difficulty = potential_contract.difficulty

			# generate pokemon rarity, pokemon, stat, happiness, payment
			stats = ['smart', 'cool', 'beauty', 'cute', 'tough']
			if difficulty == 1:
				pokemon_rarity = random.randint(1, 2)
				requested_pokemon = Pokemon.objects.filter(rarity=pokemon_rarity, basic=True).order_by('?').first()
				payment_amount = random.randint(2000, 6000)
				if pokemon_rarity == 1:
					requested_happiness = random.randint(1, 20)
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, requested_happiness=requested_happiness, difficulty=difficulty, payment_amount=payment_amount)
					return redirect(daycare)
				else:
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, difficulty=difficulty, payment_amount=payment_amount)
					return redirect(daycare)

			elif difficulty == 2:
				pokemon_rarity = random.randint(1, 3)
				requested_pokemon = Pokemon.objects.filter(rarity=pokemon_rarity, basic=True).order_by('?').first()
				payment_amount = random.randint(4000, 10000)
				if pokemon_rarity == 1:
					requested_happiness = random.randint(20, 40)
					requested_stat = random.choice(stats)
					requested_stat_value = random.randint(20, 40)
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, requested_happiness=requested_happiness, requested_stat=requested_stat, requested_stat_value=requested_stat_value, difficulty=difficulty, payment_amount=payment_amount)
					return redirect(daycare)
				elif pokemon_rarity == 2:
					requested_happiness = random.randint(20, 40)
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, requested_happiness=requested_happiness, difficulty=difficulty, payment_amount=payment_amount)
					return redirect(daycare)
				else:
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, difficulty=difficulty, payment_amount=payment_amount)
					return redirect(daycare)

			elif difficulty == 3:
				pokemon_rarity = random.randint(2, 4)
				requested_pokemon = Pokemon.objects.filter(rarity=pokemon_rarity, basic=True).order_by('?').first()
				payment_method = random.randint(1, 4)
				if payment_method <= 3:
					payment_method = "PD"
					payment_amount = random.randint(10000, 15000)
				else:
					payment_method = "coins"
					payment_amount = random.randint(10, 50)

				if pokemon_rarity == 2:
					requested_happiness = random.randint(40, 60)
					requested_stat = random.choice(stats)
					requested_stat_value = random.randint(40, 60)
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, requested_happiness=requested_happiness, requested_stat=requested_stat, requested_stat_value=requested_stat_value, difficulty=difficulty, payment_method=payment_method, payment_amount=payment_amount)
					return redirect(daycare)
				elif pokemon_rarity == 3:
					requested_happiness = random.randint(40, 60)
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, requested_happiness=requested_happiness, difficulty=difficulty, payment_method=payment_method, payment_amount=payment_amount)
					return redirect(daycare)
				else:
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, difficulty=difficulty, payment_method=payment_method, payment_amount=payment_amount)
					return redirect(daycare)

			elif difficulty == 4:
				pokemon_rarity = random.randint(3, 5)
				requested_pokemon = Pokemon.objects.filter(rarity=pokemon_rarity, basic=True).order_by('?').first()
				payment_method = random.randint(1, 4)
				if payment_method <= 3:
					payment_method = "PD"
					payment_amount = random.randint(16000, 20000)
				else:
					payment_method = "coins"
					payment_amount = random.randint(40, 80)

				if pokemon_rarity == 3:
					requested_happiness = random.randint(60, 80)
					requested_stat = random.choice(stats)
					requested_stat_value = random.randint(60, 80)
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, requested_happiness=requested_happiness, requested_stat=requested_stat, requested_stat_value=requested_stat_value, difficulty=difficulty, payment_method=payment_method, payment_amount=payment_amount)
					return redirect(daycare)
				elif pokemon_rarity == 4:
					requested_happiness = random.randint(60, 80)
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, requested_happiness=requested_happiness, difficulty=difficulty, payment_method=payment_method, payment_amount=payment_amount)
					return redirect(daycare)
				else:
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, difficulty=difficulty, payment_method=payment_method, payment_amount=payment_amount)
					return redirect(daycare)

			else: # difficulty == 5
				pokemon_rarity = random.randint(4, 5)
				requested_pokemon = Pokemon.objects.filter(rarity=pokemon_rarity, basic=True).order_by('?').first()
				payment_method = random.randint(1, 4)
				if payment_method <= 3:
					payment_method = "PD"
					payment_amount = random.randint(23000, 28000)
				else:
					payment_method = "coins"
					payment_amount = random.randint(70, 120)

				if pokemon_rarity == 4:
					requested_happiness = random.randint(80, 100)
					requested_stat = random.choice(stats)
					requested_stat_value = random.randint(80, 100)
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, requested_happiness=requested_happiness, requested_stat=requested_stat, requested_stat_value=requested_stat_value, difficulty=difficulty, payment_method=payment_method, payment_amount=payment_amount)
					return redirect(daycare)
				else:
					requested_happiness = random.randint(80, 100)
					potential_contract.delete()
					contract = Contract.objects.create(user=request.user, requested_pokemon=requested_pokemon, requested_happiness=requested_happiness, difficulty=difficulty, payment_method=payment_method, payment_amount=payment_amount)
					return redirect(daycare)

		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def reject_potential_contract(request):
	if request.user.is_authenticated():
		potential_contract = PotentialContract.objects.filter(user=request.user)
		if potential_contract.exists():
			potential_contract = potential_contract.first()
			potential_contract.delete()
			return redirect(daycare)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def cancel_contract(request):
	if request.user.is_authenticated():
		contract = Contract.objects.filter(user=request.user)
		currency = Currency.objects.get(user=request.user)
		if currency.pd >= 1000:
			if contract.exists():
				contract = contract.first()
				currency.spend_pd(1000)
				contract.delete()
				return redirect(daycare)
			else:
				return redirect(daycare)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def complete_contract_page(request):
	if request.user.is_authenticated():
		action = "Completing a contract"
		update_online(request, action)

		contract = Contract.objects.filter(user=request.user).exists()
		if contract:
			adopts_in_party = Adopt.objects.filter(owner=request.user, hatched=True, party=True, gts=False, daycare=False)
			boxes = Box.objects.filter(user=request.user)
			return render(request, 'site/complete_contract.html', {'boxes':boxes, 'adopts_in_party':adopts_in_party})
		else:
			return redirect(daycare)
	else:
		return redirect(must_be_logged_in)

def complete_contract(request):
	if request.user.is_authenticated():
		contract = Contract.objects.filter(user=request.user)
		if contract.exists():
			contract = contract.first()
			adopt_pk = request.POST.get("adopt_pk")
			adopt = Adopt.objects.filter(pk=adopt_pk)
			if adopt.exists():
				adopt = adopt.first()
				if adopt.owner == request.user:
					requested_pokemon = False
					requested_happiness = False
					requested_stat = False
					requested_date = False

					if adopt.pokemon == contract.requested_pokemon:
						requested_pokemon = True

					if contract.requested_happiness:
						if adopt.happiness >= contract.requested_happiness:
							requested_happiness = True
					else:
						requested_happiness = True

					if contract.requested_stat:
						if contract.requested_stat == "smart":
							if adopt.smart >= contract.requested_stat_value:
								requested_stat = True
						elif contract.requested_stat == "cool":
							if adopt.cool >= contract.requested_stat_value:
								requested_stat = True
						elif contract.requested_stat == "beauty":
							if adopt.beauty >= contract.requested_stat_value:
								requested_stat = True
						elif contract.requested_stat == "cute":
							if adopt.cute >= contract.requested_stat_value:
								requested_stat = True
						elif contract.requested_stat == "tough":
							if adopt.tough >= contract.requested_stat_value:
								requested_stat = True
					else:
						requested_stat = True

					if adopt.hatch_time > contract.date_accepted:
						requested_date = True

					if requested_pokemon and requested_happiness and requested_stat and requested_date:
						currency = Currency.objects.get(user=request.user)
						if contract.payment_method == "PD":
							currency.get_pd(contract.payment_amount)
						elif contract.payment_method == "coins":
							currency.get_coins(contract.payment_amount)

						if contract.difficulty == 3:
							parcel = Item.objects.filter(name="parcel").first()
							has_parcel = Inventory.objects.filter(user=request.user, item=parcel)
							if has_parcel.count() != 0:
								parcel = has_parcel.first()
								parcel.quantity += 1
								parcel.save()
							else:
								parcel = Inventory.objects.create(user=request.user, item=parcel, quantity=1)

						elif contract.difficulty == 4:
							parcel = Item.objects.filter(name="parcel").first()
							has_parcel = Inventory.objects.filter(user=request.user, item=parcel)
							if has_parcel.count() != 0:
								parcel = has_parcel.first()
								parcel.quantity += 3
								parcel.save()
							else:
								parcel = Inventory.objects.create(user=request.user, item=parcel, quantity=3)

						elif contract.difficulty == 5:
							parcel = Item.objects.filter(name="parcel").first()
							has_parcel = Inventory.objects.filter(user=request.user, item=parcel)
							if has_parcel.count() != 0:
								parcel = has_parcel.first()
								parcel.quantity += 5
								parcel.save()
							else:
								parcel = Inventory.objects.create(user=request.user, item=parcel, quantity=5)

						adopt.delete()
						contract.delete()
						return redirect(daycare)
					else:
						return redirect(daycare)
				else:
					return redirect(daycare)
			else:
				return redirect(daycare)
		else:
			return redirect(daycare)
	else:
		return redirect(must_be_logged_in)

# POKERADAR VIEWS

def pokeradar(request):
	if request.user.is_authenticated():
		action = "Checking the Pok&eacute; Radar"
		update_online(request, action)

		poke_radar = Item.objects.filter(image="poke-radar")
		check_for_radar = Inventory.objects.filter(user=request.user, item=poke_radar)
		if check_for_radar.count() != 0:
			check_for_dex = Dex.objects.filter(user=request.user)
			if check_for_dex.count() != 0:
				dex = check_for_dex.first()

				basic_pokemon = Pokemon.objects.filter(basic=True)
				basic_pokemon_in_dex = []

				for pokemon in basic_pokemon:
					if dex.pokemon.filter(name=pokemon.name).exists():
						basic_pokemon_in_dex.append(pokemon)

				check_for_hunt = Hunt.objects.filter(user=request.user)
				if check_for_hunt.count() != 0:
					hunt = check_for_hunt.first()
					charge_percent = (hunt.charge / 300)*100

					time_threshold = timezone.now() - timedelta(hours=24)
					shiny_charm = ShinyCharm.objects.filter(user=request.user, start_time__gte=time_threshold)
					if shiny_charm.count() != 0:
						shiny_charm = shiny_charm.first()
					else:
						shiny_charm = None

					if hunt.hatched is not 0:
						if check_yesterday_hatched():
							if shiny_charm is not None:
								shiny_chance = (1 / (250/hunt.hatched))*100
							else:
								shiny_chance = (1 / (500/hunt.hatched))*100
						else:
							if shiny_charm is not None:
								shiny_chance = (1 / (500/hunt.hatched))*100
							else:
								shiny_chance = (1 / (1000/hunt.hatched))*100
					else:
						shiny_chance = 0.0

					if check_yesterday_hatched():
						if shiny_charm is not None:
							if shiny_chance > 10.0:
								shiny_chance == 20.0
						else:
							if shiny_chance > 5.0:
								shiny_chance = 10.0
					else:
						if shiny_charm is not None:
							if shiny_chance > 10.0:
								shiny_chance = 10.0
						else:
							if shiny_chance > 5.0:
								shiny_chance = 5.0

					if hunt.second_hatched is not 0:
						if check_yesterday_hatched():
							if shiny_charm is not None:
								second_shiny_chance = (1 / (250/hunt.second_hatched))*100
							else:
								second_shiny_chance = (1 / (500/hunt.second_hatched))*100
						else:
							if shiny_charm is not None:
								second_shiny_chance = (1 / (500/hunt.second_hatched))*100
							else:
								second_shiny_chance = (1 / (1000/hunt.second_hatched))*100
					else:
						second_shiny_chance = 0.0

					if check_yesterday_hatched():
						if shiny_charm is not None:
							if second_shiny_chance > 10.0:
								second_shiny_chance == 20.0
						else:
							if second_shiny_chance > 5.0:
								second_shiny_chance = 10.0
					else:
						if shiny_charm is not None:
							if second_shiny_chance > 10.0:
								second_shiny_chance = 10.0
						else:
							if second_shiny_chance > 5.0:
								second_shiny_chance = 5.0

					shiny_day = check_yesterday_hatched()

					poke_radar_items = Item.objects.filter(category="poke radar item")

					gold_batteries = Item.objects.filter(name="gold batteries")
					has_gold_batteries = Inventory.objects.filter(user=request.user, item=gold_batteries)
					if has_gold_batteries.count() != 0:
						has_gold_batteries = True
					else:
						has_gold_batteries = False

					radar_drive = Item.objects.filter(name="radar drive")
					has_radar_drive = Inventory.objects.filter(user=request.user, item=radar_drive)
					if has_radar_drive.count() != 0:
						has_radar_drive = True
					else:
						has_radar_drive = False

					shiny_charm_item = Item.objects.filter(name="shiny charm")
					has_shiny_charm = Inventory.objects.filter(user=request.user, item=shiny_charm_item)
					if has_shiny_charm.count() != 0:
						has_shiny_charm = has_shiny_charm.first()
					else:
						has_shiny_charm = None

					return render(request, 'site/pokeradar.html', {'basic_pokemon_in_dex':basic_pokemon_in_dex, 'hunt':hunt, 'charge_percent':charge_percent, 'shiny_chance':shiny_chance, 'second_shiny_chance':second_shiny_chance, 'shiny_day':shiny_day, 'poke_radar_items':poke_radar_items, 'has_gold_batteries':has_gold_batteries, 'has_radar_drive':has_radar_drive, 'shiny_charm':shiny_charm, 'has_shiny_charm':has_shiny_charm})
				else:
					poke_radar_items = Item.objects.filter(category="poke radar item")
					return render(request, 'site/pokeradar.html', {'basic_pokemon_in_dex':basic_pokemon_in_dex, 'poke_radar_items':poke_radar_items})

			else:
				return redirect(pokedex)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def start_hunt(request):
	if request.user.is_authenticated():
		poke_radar = Item.objects.filter(image="poke-radar")
		check_for_radar = Inventory.objects.filter(user=request.user, item=poke_radar)
		if check_for_radar.count() != 0:
			check_for_dex = Dex.objects.filter(user=request.user)
			if check_for_dex.count() != 0:
				pokemon_number = request.POST.get('pokemon')
				pokemon = Pokemon.objects.filter(number=pokemon_number).first()
				dex = check_for_dex.first()
				if dex.pokemon.filter(number=pokemon_number).exists():
					hunt = Hunt.objects.create(user=request.user, pokemon=pokemon)
					return redirect(pokeradar)
				else:
					return redirect(cannot_access)
			else:
				return redirect(pokedex)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def add_second_pokemon_to_hunt(request):
	if request.user.is_authenticated():
		poke_radar = Item.objects.filter(image="poke-radar")
		check_for_radar = Inventory.objects.filter(user=request.user, item=poke_radar)
		if check_for_radar.count() != 0:
			check_for_dex = Dex.objects.filter(user=request.user)
			if check_for_dex.count() != 0:
				hunt = Hunt.objects.filter(user=request.user)
				if hunt.count() != 0:
					hunt = hunt.first()
					pokemon_number = request.POST.get('pokemon')
					pokemon = Pokemon.objects.filter(number=pokemon_number).first()
					hunt.add_second_pokemon(pokemon)

					return redirect(pokeradar)
				else:
					return redirect(pokeradar)
			else:
				return redirect(pokedex)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def cancel_hunt(request):
	if request.user.is_authenticated():
		hunt = Hunt.objects.filter(user=request.user)
		if hunt.count() != 0:
			hunt = hunt.first()
			hunt.delete()
			return redirect(pokeradar)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def cancel_second_hunt(request):
	if request.user.is_authenticated():
		hunt = Hunt.objects.filter(user=request.user)
		if hunt.count() != 0:
			hunt = hunt.first()
			hunt.second_pokemon = None
			hunt.second_hatched = 0
			hunt.save()
			return redirect(pokeradar)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def activate_shiny_charm(request):
	if request.user.is_authenticated():
		shiny_charm_item = Item.objects.get(name="shiny charm")
		shiny_charm = Inventory.objects.filter(user=request.user, item=shiny_charm_item)
		if shiny_charm.count() != 0:
			shiny_charm = shiny_charm.first()
			if shiny_charm.quantity > 1:
				shiny_charm.quantity -= 1
				shiny_charm.save()
			else:
				shiny_charm.delete()

			charm = ShinyCharm.objects.create(user=request.user)
			return redirect(pokeradar)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

# GTS VIEWS

def gts(request):
	if request.user.is_authenticated():
		action = "Visiting the GTS"
		update_online(request, action)

		sent_trades = Trade.objects.filter(sending_user=request.user, seen_offer=False)
		recieved_trades = Trade.objects.filter(recieving_user=request.user, seen_final=False)

		return render(request, 'site/gts.html', {'sent_trades':sent_trades, 'recieved_trades':recieved_trades})
	else:
		return redirect(must_be_logged_in)

def start_trade_page(request, username=""):
	if request.user.is_authenticated():
		boxes = Box.objects.filter(user=request.user)
		adopts_in_party = Adopt.objects.filter(owner=request.user, hatched=True, party=True, gts=False, daycare=False)
		return render(request, 'site/start_trade.html', {'boxes':boxes, 'username':username, 'adopts_in_party':adopts_in_party})
	else:
		return redirect(must_be_logged_in)

def start_trade(request):
	if request.user.is_authenticated():
		adopt_pk = request.POST.get("adopt_pk")
		adopt = Adopt.objects.filter(pk=adopt_pk)
		if adopt.count() != 0:
			adopt = adopt.first()
			recieving_user = request.POST.get("username")
			recieving_user = User.objects.filter(username=recieving_user)
			if recieving_user.count() != 0:
				recieving_user = recieving_user.first()
				message = request.POST.get("message")

				trade = Trade.objects.create(sending_user=request.user, recieving_user=recieving_user, sending_adopt=adopt, sending_message=message)
				adopt.gts = True
				adopt.save()
				return redirect(gts)

			else:
				return redirect(user_not_found)
		else:
			return redirect(start_trade_page)
	else:
		return redirect(must_be_logged_in)

def cancel_trade(request, pk):
	if request.user.is_authenticated():
		trade = Trade.objects.filter(pk=pk)
		if trade.count() != 0:
			trade = trade.first()
			if trade.sending_user == request.user:
				if not trade.sending_adopt.party:
					trade.delete()
					trade.sending_adopt.gts = False
					trade.sending_adopt.save()
					return redirect(gts)
				else:
					party_pokemon = Adopt.objects.filter(user=request.user, part=True, gts=False, daycare=False)
					if party_pokemon < 6:
						trade.delete()
						trade.sending_adopt.gts = False
						trade.sending_adopt.save()
						return redirect(gts)
					else:
						return redirect(party_is_full)
			else:
				return redirect(cannot_access)
		else:
			return redirect(gts)
	else:
		return redirect(must_be_logged_in)

def offer_trade_page(request, pk):
	if request.user.is_authenticated():
		boxes = Box.objects.filter(user=request.user)
		adopts_in_party = Adopt.objects.filter(owner=request.user, hatched=True, party=True, gts=False, daycare=False)
		trade = Trade.objects.filter(pk=pk).first()
		if trade.recieving_user == request.user:
			return render(request, 'site/offer_trade.html', {'boxes':boxes, 'trade':trade, 'adopts_in_party':adopts_in_party})
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def offer_trade(request, pk):
	if request.user.is_authenticated():
		trade = Trade.objects.filter(pk=pk).first()
		if trade.recieving_user == request.user:
			adopt_pk = request.POST.get("adopt_pk")
			adopt = Adopt.objects.filter(pk=adopt_pk)
			if adopt.count() != 0:
				adopt = adopt.first()
				message = request.POST.get("message")
				trade.add_offer(adopt, message)
				adopt.gts = True
				adopt.save()
				return redirect(gts)
			else:
				return redirect(gts)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def accept_trade_offer(request, pk):
	if request.user.is_authenticated():
		trade = Trade.objects.filter(pk=pk).first()
		if trade.sending_user == request.user:
			party_pokemon = Adopt.objects.filter(owner=request.user, party=True).count()
			if party_pokemon < 6:
				trade.seen_offer = True
				trade.accepted = True
				trade.save()
				trade.recieving_adopt.change_owner(request.user)
				trade.sending_adopt.change_owner(trade.recieving_user)
				trade.recieving_adopt.gts = False
				trade.recieving_adopt.save()

				if trade.recieving_adopt.pokemon.evo_on_trade:
					trade.recieving_adopt.ready_to_evo_by_trade = True
					trade.recieving_adopt.save()
				if trade.sending_adopt.pokemon.evo_on_trade:
					trade.sending_adopt.ready_to_evo_by_trade = True
					trade.sending_adopt.save()

				dex = Dex.objects.filter(user=request.user)
				if dex.count() is not 0:
					dex = dex.first()
					dex_pokemon_entry = dex.pokemon.filter(name=trade.recieving_adopt.pokemon.name).exists()
					if not dex_pokemon_entry:
						dex.add_pokemon_entry(trade.recieving_adopt.pokemon)

				recieving_box_list = Box.objects.filter(user=trade.recieving_user)
				for box in recieving_box_list:
					if box.pokemon.filter(pk=trade.recieving_adopt.pk).exists():
						box.remove_pokemon(trade.recieving_adopt)
				sending_box_list = Box.objects.filter(user=trade.sending_user)
				for box in sending_box_list:
					if box.pokemon.filter(pk=trade.sending_adopt.pk).exists():
						box.remove_pokemon(trade.sending_adopt)

				return redirect(profile_page, username=request.user.username)
			else: 
				return redirect(gts)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def reject_trade_offer(request, pk):
	if request.user.is_authenticated():
		trade = Trade.objects.filter(pk=pk).first()
		if trade.sending_user == request.user:
			party_pokemon = Adopt.objects.filter(owner=request.user, party=True).count()
			if party_pokemon < 6:
				trade.seen_offer = True
				trade.rejected = True
				trade.save()
				trade.sending_adopt.gts = False
				trade.sending_adopt.save()
				trade.sending_adopt.from_box_to_party()

				recieving_box_list = Box.objects.filter(user=trade.recieving_user)
				for box in recieving_box_list:
					if box.pokemon.filter(pk=trade.recieving_adopt.pk).exists():
						box.remove_pokemon(trade.recieving_adopt)
				sending_box_list = Box.objects.filter(user=trade.sending_user)
				for box in sending_box_list:
					if box.pokemon.filter(pk=trade.sending_adopt.pk).exists():
						box.remove_pokemon(trade.sending_adopt)

				return redirect(profile_page, username=request.user.username)
			else:
				return redirect(gts)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def collect_trade_offer(request, pk):
	if request.user.is_authenticated():
		trade = Trade.objects.filter(pk=pk).first()
		if trade.recieving_user == request.user:
			party_pokemon = Adopt.objects.filter(owner=request.user, party=True, gts=False, daycare=False).count()
			if party_pokemon < 6:
				trade.seen_final = True
				trade.save()
				trade.sending_adopt.gts = False
				trade.sending_adopt.save()

				dex = Dex.objects.filter(user=request.user)
				if dex.count() is not 0:
					dex = dex.first()
					dex_pokemon_entry = dex.pokemon.filter(name=trade.sending_adopt.pokemon.name).exists()
					if not dex_pokemon_entry:
						dex.add_pokemon_entry(trade.sending_adopt.pokemon)

				return redirect(profile_page, username=request.user.username)
			else: 
				return redirect(gts)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def collect_rejected_trade_offer(request, pk):
	if request.user.is_authenticated():
		trade = Trade.objects.filter(pk=pk).first()
		if trade.recieving_user == request.user:
			party_pokemon = Adopt.objects.filter(owner=request.user, party=True, gts=False, daycare=False).count()
			if party_pokemon < 6:
				trade.seen_final = True
				trade.save()
				trade.recieving_adopt.gts = False
				trade.recieving_adopt.save()
				trade.recieving_adopt.from_box_to_party()

				return redirect(profile_page, username=request.user.username)
			else: 
				return redirect(gts)
		else:
			return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)



def pokemon_web_scrape(request):

	url = "https://pokemondb.net/pokedex/national"

	req = urllib2.Request(url, headers={'user-Agent' : 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'})
	page_html = urllib2.urlopen(req).read()

	html_dom = etree.HTML(page_html)

	url_results = {}
	all_names = html_dom.xpath('//a[@class="ent-name"]/text()')

	for name in all_names:
		number = html_dom.xpath('//a[text() = "'+name+'"]/../small[1]/text()')[0]
		primary_type = html_dom.xpath('//a[text() = "'+name+'"]/../small[@class="aside"]/a[1]/text()')[0]
		secondary_type = html_dom.xpath('//a[text() = "'+name+'"]/../small[@class="aside"]/a[2]/text()')
		if secondary_type:
			secondary_type = secondary_type[0]
		else:
			secondary_type = ""

		format_number = int(number.strip("#").rstrip("0"))
		url_results[name] = [format_number, primary_type, secondary_type]

	scraped_pokemon = [
		Scraped(
			name=name,
			number=data[0],
			primary_type=data[1],
			secondary_type=data[2]
		)
		for name, data in url_results.items()
	]

	# scrape = Pokemon.objects.bulk_create(scraped_pokemon)

	return redirect(lab)












