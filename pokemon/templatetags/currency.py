from django.template import Library

from core.models import Currency

register = Library()

@register.filter(name="currency_pd")
def currency(user):
	currency = Currency.objects.filter(user=user).first()
	pd = currency.pd
	return pd

@register.filter(name="currency_coins")
def currency(user):
	currency = Currency.objects.filter(user=user).first()
	coins = currency.coins
	return coins