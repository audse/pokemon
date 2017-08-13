from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

	# STATIC PAGES
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login_page, name='login_page'),
	url(r'^register/$', views.register_page, name='register_page'),
	url(r'^user/(?P<username>.*)/$', views.profile_page, name='profile_page'),
	url(r'^load/(?P<pk>[0-9]+)/$', views.load_box, name='load_box'),
	url(r'^users/online/$', views.online_page, name='online_page'),

	# FUNCTION PAGES
	url(r'^login/auth/$', views.login, name='login'),
	url(r'^logout/auth/$', views.logout, name='logout'),
	url(r'^register/auth/$', views.register, name='register'),
	url(r'^about/edit/$', views.edit_about, name='edit_about'),
	url(r'^update/action/$', views.manually_update_online, name='manually_update_online'),

	# ERROR PAGES
	url(r'^error/auth/none/$', views.must_be_logged_in, name='must_be_logged_in'),
	url(r'^error/auth/toomuch/$', views.cannot_be_logged_in, name='cannot_be_logged_in'),
	url(r'^error/user/none/$', views.user_not_found, name='user_not_found'),
	url(r'^login/failed/$', views.login_failed, name='login_failed'),
	url(r'^error/interaction/$', views.cannot_interact, name='cannot_interact'),
	url(r'^error/auth/$', views.cannot_access, name='cannot_access'),
	url(r'^error/auth/staff$', views.staff_only, name='staff_only'),
	url(r'^error/party/$', views.party_is_full, name='party_is_full'),

	# LAB PAGES
	url(r'^lab/$', views.lab, name='lab'),
	url(r'^lab/reload/$', views.lab_reload, name='lab_reload'),
	url(r'^lab/adopt/(?P<pk>[0-9]+)/$', views.lab_adopt, name='lab_adopt'),
	url(r'^lab/summon/(?P<item_pk>[0-9]+)/$', views.summon_pokemon, name='summon_pokemon'),

	# INTERACTING WITH ADOPTS PAGES
	url(r'^pokemon/interact/$', views.interact, name='interact'),
	url(r'^(?P<status>.*)/view/(?P<pk>[0-9]+)/$', views.view_adopt, name='view_adopt'),
	url(r'^pokemon/view/(?P<pk>[0-9]+)/nickname/$', views.change_nickname, name='change_nickname'),
	url(r'^pokemon/evolve/exp/(?P<pk>[0-9]+)/$', views.evolve_by_level, name='evolve_by_level'),
	url(r'^pokemon/evolve/item/(?P<pk>[0-9]+)/$', views.evolve_by_item, name='evolve_by_item'),
	url(r'^pokemon/evolve/eevee/(?P<pk>[0-9]+)/(?P<item>.*)/$', views.evolve_eevee, name='evolve_eevee'),
	url(r'^pokemon/evolve/trade/(?P<pk>[0-9]+)/$', views.evolve_by_trade, name='evolve_by_trade'),
	url(r'^egg/hatch/(?P<pk>[0-9]+)/$', views.hatch_egg, name='hatch_egg'),
	url(r'^pokemon/view/(?P<adopt_pk>[0-9]+)/item/$', views.give_held_item, name='give_held_item'),
	url(r'^pokemon/view/(?P<adopt_pk>[0-9]+)/item/take/$', views.take_held_item, name='take_held_item'),

	# BOXES PAGES
	url(r'^boxes/$', views.boxes, name='boxes'),
	url(r'^boxes/create/$', views.create_box_page, name='create_box_page'),
	url(r'^boxes/edit/(?P<pk>[0-9]+)/$', views.edit_box, name='edit_box'),
	url(r'^boxes/delete/(?P<pk>[0-9]+)/$', views.delete_box, name='delete_box'),
	url(r'^boxes/create/processsing/$', views.create_box, name='create_box'),
	url(r'^boxes/(?P<box>[0-9]+)/move/(?P<adopt>[0-9]+)/$', views.move_to_box, name='move_to_box'),
	url(r'^boxes/switch/(?P<box>[0-9]+)/move/(?P<adopt>[0-9]+)/$', views.move_to_different_box, name='move_to_different_box'),
	url(r'^boxes/move/(?P<adopt>[0-9]+)/$', views.move_to_party, name='move_to_party'),

	# POKEDEX PAGES
	url(r'^dex/$', views.pokedex_index, name='pokedex_index'),
	url(r'^dex/receive/$', views.receive_pokedex, name='receive_pokedex'),

	# INVENTORY PAGES
	url(r'^inventory/$', views.inventory, name='inventory'),
	url(r'^inventory/receive/$', views.receive_bag, name='receive_bag'),
	url(r'^inventory/sell/(?P<item_pk>[0-9]+)$', views.sell_item, name='sell_item'),
	url(r'^inventory/parcel/$', views.parcel_page, name='parcel_page'),
	url(r'^inventory/parcel/open/$', views.open_parcel, name='open_parcel'),
	url(r'^inventory/parcel/parcel/open/$', views.open_parcel_parcel, name='open_parcel_parcel'),

	# POKEMART PAGES
	url(r'^pokemart/$', views.pokemart, name='pokemart'),
	url(r'^purchase/(?P<item_pk>[0-9]+)$', views.purchase_item, name='purchase_item'),
	url(r'^gold/purchase/(?P<item_pk>[0-9]+)$', views.purchase_gold_item, name='purchase_gold_item'),

	# PARK PAGES
	url(r'^park/$', views.park, name='park'),
	url(r'^park/adopt/(?P<pk>[0-9]+)/$', views.park_adopt, name='park_adopt'),
	url(r'^pokemon/view/(?P<pk>[0-9]+)/release$', views.release_adopt, name='release_adopt'),
	url(r'^park/pass/$', views.receive_park_pass, name='receive_park_pass'),
	url(r'^park/incense/$', views.park_incense, name='park_incense'),
	url(r'^park/repel/$', views.park_repel, name='park_repel'),

	# DAYCARE PAGES
	url(r'^daycare/$', views.daycare, name='daycare'),
	url(r'^daycare/dropoff/$', views.drop_off_adopt_page, name='drop_off_adopt_page'),
	url(r'^daycare/dropoff/processing/$', views.drop_off_adopt, name='drop_off_adopt'),
	url(r'^daycare/pickup/(?P<pk>[0-9]+)/$', views.pick_up_adopt, name='pick_up_adopt'),
	url(r'^daycare/adopt/(?P<pk>[0-9]+)/$', views.adopt_daycare_egg, name='adopt_daycare_egg'),
	url(r'^daycare/feed/(?P<adopt_pk>[0-9]+)/$', views.feed_poke_puff, name='feed_poke_puff'),
	url(r'^daycare/contract/$', views.create_potential_contract, name='create_potential_contract'),
	url(r'^daycare/contract/accept/$', views.accept_potential_contract, name='accept_potential_contract'),
	url(r'^daycare/contract/reject/$', views.reject_potential_contract, name='reject_potential_contract'),
	url(r'^daycare/contract/cancel/$', views.cancel_contract, name='cancel_contract'),
	url(r'^daycare/contract/complete/$', views.complete_contract_page, name='complete_contract_page'),
	url(r'^daycare/contract/complete/processing/$', views.complete_contract, name='complete_contract'),

	# POKERADAR PAGES
	url(r'^pokeradar/$', views.pokeradar, name='pokeradar'),
	url(r'^pokeradar/hunt/$', views.start_hunt, name='start_hunt'),
	url(r'^pokeradar/hunt/cancel/$', views.cancel_hunt, name='cancel_hunt'),
	url(r'^pokeradar/hunt/add/$', views.add_second_pokemon_to_hunt, name='add_second_pokemon_to_hunt'),
	url(r'^pokeradar/hunt/second/cancel/$', views.cancel_second_hunt, name='cancel_second_hunt'),
	url(r'^pokeradar/charm/$', views.activate_shiny_charm, name='activate_shiny_charm'),

	# GTS PAGES
	url(r'^gts/$', views.gts, name='gts'),
	url(r'^gts/trade/start/(?P<username>.*)$', views.start_trade_page, name='start_trade_page'),
	url(r'^gts/trade/processing/$', views.start_trade, name='start_trade'),
	url(r'^gts/trade/(?P<pk>[0-9]+)/offer/$', views.offer_trade_page, name='offer_trade_page'),
	url(r'^gts/trade/(?P<pk>[0-9]+)/cancel/$', views.cancel_trade, name='cancel_trade'),
	url(r'^gts/trade/(?P<pk>[0-9]+)/offer/processing/$', views.offer_trade, name='offer_trade'),
	url(r'^gts/trade/(?P<pk>[0-9]+)/accept/$', views.accept_trade_offer, name='accept_trade_offer'),
	url(r'^gts/trade/(?P<pk>[0-9]+)/reject/$', views.reject_trade_offer, name='reject_trade_offer'),
	url(r'^gts/trade/(?P<pk>[0-9]+)/collect/$', views.collect_trade_offer, name='collect_trade_offer'),
	url(r'^gts/trade/(?P<pk>[0-9]+)/collect/reject/$', views.collect_rejected_trade_offer, name='collect_rejected_trade_offer'),

	# EVENT PAGES
	url(r'^interactions/$', views.todays_interactions, name='todays_interactions'),

	# WEB SCRAPE
	url(r'^web/scrape/data/$', views.pokemon_web_scrape, name='pokemon_web_scrape'),
]




