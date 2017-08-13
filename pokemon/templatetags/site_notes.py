from django.template import Library

from pokedex.models import Trade, Adopt
from pm.models import PM

register = Library()

@register.filter(name="trade_notes")
def trade_notes(user):
	notifications = 0

	sent_trades = Trade.objects.filter(sending_user=user)
	recieved_trades = Trade.objects.filter(recieving_user=user)

	for trade in sent_trades:
		if not trade.accepted and not trade.rejected:
			if trade.seen_trade:
				notifications = notifications + 1

	for trade in recieved_trades:
		if not trade.accepted and not trade.rejected:
			if not trade.seen_trade:
				notifications = notifications + 1
			if trade.seen_trade and trade.seen_final:
				notifications = notifications + 1
		else:
			if not trade.seen_final:
				notifications = notifications + 1

	return notifications

@register.filter(name="hatch_notes")
def hatch_notes(user):
	notifications = 0
	eggs = Adopt.objects.filter(owner=user, party=True, gts=False, hatched=False)
	for egg in eggs:
		if egg.exp == egg.pokemon.ehp:
			notifications = notifications + 1

	return notifications

@register.filter(name="pm_notes")
def pm_notes(user):
	pms = PM.objects.filter(receiving_user=user, seen=False, removed_by_receiver=False)
	return pms.count()








