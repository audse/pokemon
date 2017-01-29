from __future__ import division
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import Action, Currency, Item, Inventory
from pokedex.models import Pokemon, Adopt, Lab, Interaction, Box, Dex

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import datetime
from datetime import timedelta
from django.utils import timezone
import random

# FUNCTIONS

def update_online(request, action="Viewing Pok&eacute;frame", override=False):
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

def check_interaction(request, adopt):
	if not adopt.hatched:
		adopt.percent = adopt.exp/adopt.pokemon.ehp*100
	else:
		get_likes(adopt)

		if adopt.pokemon.evo_level:
			adopt.percent = adopt.exp/adopt.total_exp*100
		else:
			adopt.percent = 100

	# make sure they havent interacted in the past day
	if request.user.is_authenticated():
		time_threshold = datetime.datetime.now() - timedelta(days=1)
		interactions_since_yesterday = Interaction.objects.filter(recieving_user=adopt.owner.username, sending_user=request.user, adopt=adopt, time__gte=time_threshold).count()
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
			adopts = Adopt.objects.filter(owner=user, party=True)
			for adopt in adopts:
				check_interaction(request, adopt)
		else:
			return redirect(lab)

		return render(request, 'core/profile.html', {'current_user':user, 'adopts':adopts})
	else:
		return redirect(user_not_found)

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
			user.save()
			account_currency.save()
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



# LAB VIEWS

def update_lab(request):
	lab_set = Lab.objects.get(user=request.user)
	if lab_set:

		rarity_level = []
		rarities = []

		for x in range(0, 4):
			rarities.append(random.randint(1, 1000))

		for rarity in rarities:
			if rarity < 700:
				rarity_level.append(1)
			elif rarity < 910:
				rarity_level.append(2)
			elif rarity < 973:
				rarity_level.append(3)
			elif rarity < 992:
				rarity_level.append(4)
			elif rarity < 999:
				rarity_level.append(5)
			elif rarity <= 1000:
				rarity_level.append(6)

		egg_1 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[0]).order_by('?').first().number
		egg_2 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[1]).order_by('?').first().number
		egg_3 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[2]).order_by('?').first().number
		egg_4 = Pokemon.objects.filter(ehp__isnull=False, rarity=rarity_level[3]).order_by('?').first().number
		lab_set.update(egg_1=egg_1, egg_2=egg_2, egg_3=egg_3, egg_4=egg_4)

def lab(request):
	if request.user.is_authenticated():
		check_for_dex = Dex.objects.filter(user=request.user)
		if check_for_dex.count() != 0:
			lab_set = Lab.objects.filter(user=request.user).first()
			if lab_set:
				lab_set.egg_1_type = Pokemon.objects.get(number=lab_set.egg_1).primary_type
				lab_set.egg_2_type = Pokemon.objects.get(number=lab_set.egg_2).primary_type
				lab_set.egg_3_type = Pokemon.objects.get(number=lab_set.egg_3).primary_type
				lab_set.egg_4_type = Pokemon.objects.get(number=lab_set.egg_4).primary_type
				return render(request, 'site/lab.html', {'lab_set':lab_set})
			else:

				rarity_level = []
				rarities = []

				for x in range(0, 4):
					rarities.append(random.randint(1, 1000))

				for rarity in rarities:
					if rarity < 700:
						rarity_level.append(1)
					elif rarity < 910:
						rarity_level.append(2)
					elif rarity < 973:
						rarity_level.append(3)
					elif rarity < 992:
						rarity_level.append(4)
					elif rarity < 999:
						rarity_level.append(5)
					elif rarity <= 1000:
						rarity_level.append(6)

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
				return render(request, 'site/lab.html', {'lab_set':lab_set})
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

		amount_in_party = Adopt.objects.filter(owner=request.user, party=True).count()
		if amount_in_party < 6:

			total_exp = 0
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
			return render(request, 'error/party_is_full.html')
	else:
		return redirect(must_be_logged_in)



# INTERACTION WITH ADOPTS VIEWS

def interact(request, username, pk):
	if request.user.is_authenticated():
		berry = request.POST.get('berry')
		recieving_user = User.objects.get(username=username)
		adopt = Adopt.objects.get(pk=pk)
		if recieving_user:
			# find all interactions with this pokemon since yesterday
			# if there are any, do not let interact
			time_threshold = datetime.datetime.now() - timedelta(days=1)
			interactions_since_yesterday = Interaction.objects.filter(recieving_user=username, sending_user=request.user, adopt=adopt, time__gte=time_threshold).count()
			if interactions_since_yesterday is not 0:
				return redirect(cannot_interact)
			else:
				exp_amount = 50

				if berry == "favorite":
					exp_amount += 20
				elif berry == "disliked":
					exp_amount -= 20

				adopt.interact(exp_amount)
				interaction = Interaction.objects.create(sending_user = request.user, recieving_user=recieving_user, adopt=adopt)
				users_currency = Currency.objects.filter(user=request.user).first()
				pd_amount = random.randint(1, 5)
				users_currency.get_pd(pd_amount)

				return redirect(profile_page, username)
		else:
			return redirect(user_not_found)
	else:
		return redirect(must_be_logged_in)

def view_adopt(request, pk):
	action = "Viewing a Pok&eacute;mon summary"
	update_online(request, action)

	adopt = Adopt.objects.filter(pk=pk)
	if adopt.count() is not 0:
		adopt = adopt.first()
		if request.user.is_authenticated():
			if request.user.username == adopt.owner.username:
				boxes = Box.objects.filter(user=request.user)
			else:
				boxes = None

			check_interaction(request, adopt)
		return render(request, 'site/view_adopt.html', {'adopt':adopt, 'boxes':boxes})
	else:
		return redirect(pokemon_not_found)

def hatch_egg(request, pk):
	if request.user.is_authenticated():
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

					# select random traits for pokemon
					random_gender = random.randint(1,100)
					if random_gender <= adopt.pokemon.percent_male:
						gender = True
					else:
						gender = False

					random_shiny = random.randint(1, 1000)
					if random_shiny == 500: # 1/1000 chance
						shiny = True
					else:
						shiny = False

					random_nature = random.randint(0, 15)
					natures = ['hardy', 'lonely', 'brave', 'adamant', 'naughty', 'bold', 'docile', 'relaxed', 'impish', 'lax', 'timid', 'hasty', 'serious', 'jolly', 'naive', 'modest', 'mild', 'quiet', 'bashful', 'rash', 'calm', 'gentle', 'sassy', 'careful', 'quirky']
					nature = natures[random_nature]

					adopt.hatch(gender, shiny, nature)
					return redirect(view_adopt, pk=adopt.pk)
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
		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() is not 0:
			adopt = adopt.first()

			if adopt.pokemon.evo:
				if adopt.total_exp == adopt.exp:
					evolution = Pokemon.objects.get(number=adopt.pokemon.evo)
					adopt.evolve(evolution)

					dex = Dex.objects.filter(user=request.user)
					if dex.count() is not 0:
						dex = dex.first()
						dex_pokemon_entry = dex.pokemon.filter(name=evolution.pokemon.name).exists()
						if not dex_pokemon_entry:
							dex.add_pokemon_entry(evolution)

						return redirect(view_adopt, pk=pk)

					else:
						return redirect(pokedex_index)
				else:
					return redirect(view_adopt, pk=pk)
			else:
				return redirect(pokemon_not_found)
		else:
			return redirect(pokemon_not_found)
	else:
		return redirect(must_be_logged_in)

def change_nickname(request, pk):	
	if request.user.is_authenticated():
		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() is not 0:
			adopt = adopt.first()
			if request.user.username == adopt.owner.username:
				nickname = request.POST.get('nickname')
				adopt.change_nickname(nickname)
				return redirect(view_adopt, pk=pk)
			else:
				return redirect(cannot_access)
		else:
			return redirect(pokemon_not_found)
	else:
		return redirect(must_be_logged_in)


# BOXES VIEWS

def boxes(request):
	if request.user.is_authenticated():
		action = "Viewing boxes"
		update_online(request, action)

		boxes = Box.objects.filter(user=request.user)
		if boxes.count() is not 0:
			return render(request, 'site/boxes.html', {'boxes':boxes})
		else:
			return render(request, 'site/no_boxes.html')
	else:
		return redirect(must_be_logged_in)

def create_box_page(request):
	action = "Creating a box"
	update_online(request, action)

	return render(request, 'site/create_box_page.html')

def create_box(request):
	if request.user.is_authenticated():
		user = request.user
		box_name = request.POST.get("name")
		wallpaper = request.POST.get("wallpaper")

		box = Box.objects.create(user=user, name=box_name, wallpaper=wallpaper)
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
				box_list = Box.objects.filter(pk=box)
				if box_list.count() is 0:
					return redirect(boxes)
				else:
					box = box_list.first()
					pokemon_in_box = box.pokemon.order_by('box_pos')
					last_pokemon = pokemon_in_box.last()
					if last_pokemon:
						pos = last_pokemon.pokemon.box_pos + 1
					else:
						pos = 1

					adopt.from_party_to_box(pos)
					box.add_pokemon(adopt)
					return redirect(boxes)
			else: 
				return redirect(cannot_access)
	else:
		return redirect(must_be_logged_in)

def update_position(request):
	pk = request.POST.get('pk')
	adopt = Adopt.objects.filter(pk=pk).first()
	pos = request.GET.get('pos')

	adopt.update_box_position(pos=pos)


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
		return redirect(must_be_logged_in)

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


# PARK VIEWS

def park(request):
	cedar = User.objects.filter(username="CEDAR")
	park_pokemon = Adopt.objects.filter(owner=cedar).order_by('?')[:10]
	for pokemon in park_pokemon:
		pokemon.x_percent = random.randint(0, 100)
		pokemon.y_percent = random.randint(0, 100)

	return render(request, 'site/park.html', {'park_pokemon':park_pokemon})

def park_adopt(request, pk):
	if request.user.is_authenticated():
		adopt = Adopt.objects.filter(pk=pk)
		if adopt.count() is not 0:
			adopt = adopt.first()

			check_for_dex = Dex.objects.filter(user=request.user)
			if check_for_dex.count() != 0:

				amount_in_party = Adopt.objects.filter(owner=request.user, party=True).count()
				if amount_in_party < 6:
					adopt.change_owner(request.user)
					return redirect(park)
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
					cedar = User.objects.get(username="CEDAR")
					adopt.change_owner(cedar)
					return redirect(profile_page, username=request.user.username)
				else:
					return redirect(view_adopt, pk=pk)
			else:
				return redirect(cannot_access)
		else:
			return redirect(pokemon_not_found)
	else:
		return redirect(must_be_logged_in)













