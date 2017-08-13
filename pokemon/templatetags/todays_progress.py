from django.template import Library

from pokedex.models import Interaction, Adopt

from datetime import timedelta, time, datetime

register = Library()

@register.filter(name="todays_progress_interaction")
def todays_progress_interaction(value):
	today = datetime.now().date()
	tomorrow = today + timedelta(1)
	today_start = datetime.combine(today, time())
	today_end = datetime.combine(tomorrow, time())

	yesterday = today - timedelta(1)
	yesterday_start = datetime.combine(yesterday, time())
	yesterday_end = datetime.combine(today, time())

	day_before = today - timedelta(2)
	day_before_start = datetime.combine(day_before, time())
	day_before_end = datetime.combine(yesterday, time())

	yesterday_interactions = Interaction.objects.filter(time__gte=yesterday_start, time__lte=yesterday_end).count()
	day_before_interactions = Interaction.objects.filter(time__gte=day_before_start, time__lte=day_before_end).count()

	if yesterday_interactions < 2000:
		interactions = Interaction.objects.filter(time__gte=today_start, time__lte=today_end).count()
		return interactions/20
	else:
		if day_before_interactions >= 2000:
			interactions = Interaction.objects.filter(time__gte=today_start, time__lte=today_end).count()
			return interactions/20
		else:
			return 1000.1

@register.filter(name="todays_progress_berry_interaction")
def todays_progress_berry_interaction(value):
	today = datetime.now().date()
	tomorrow = today + timedelta(1)
	today_start = datetime.combine(today, time())
	today_end = datetime.combine(tomorrow, time())

	yesterday = today - timedelta(1)
	yesterday_start = datetime.combine(yesterday, time())
	yesterday_end = datetime.combine(today, time())

	day_before = today - timedelta(2)
	day_before_start = datetime.combine(day_before, time())
	day_before_end = datetime.combine(yesterday, time())

	yesterday_berry_interactions = Interaction.objects.filter(time__gte=yesterday_start, time__lte=yesterday_end, berry=True).count()
	day_before_berry_interactions = Interaction.objects.filter(time__gte=day_before_start, time__lte=day_before_end, berry=True).count()
	
	if yesterday_berry_interactions < 500:
		berry_interactions = Interaction.objects.filter(time__gte=today_start, time__lte=today_end, berry=True).count()
		return berry_interactions/5
	else:
		if day_before_interactions >= 500:
			berry_interactions = Interaction.objects.filter(time__gte=today_start, time__lte=today_end, berry=True).count()
			return berry_interactions/5
		else:
			return 1000.1


@register.filter(name="todays_progress_hatch")
def todays_progress_hatch(value):
	today = datetime.now().date()
	tomorrow = today + timedelta(1)
	today_start = datetime.combine(today, time())
	today_end = datetime.combine(tomorrow, time())

	yesterday = today - timedelta(1)
	yesterday_start = datetime.combine(yesterday, time())
	yesterday_end = datetime.combine(today, time())

	day_before = today - timedelta(2)
	day_before_start = datetime.combine(day_before, time())
	day_before_end = datetime.combine(yesterday, time())

	yesterday_hatched = Adopt.objects.filter(hatch_time__gte=yesterday_start, hatch_time__lte=yesterday_end).count()
	day_before_hatched = Adopt.objects.filter(hatch_time__gte=day_before_start, hatch_time__lte=day_before_end).count()

	if yesterday_hatched < 100:
		hatched = Adopt.objects.filter(hatch_time__gte=today_start, hatch_time__lte=today_end).count()
		return hatched
	else:
		if day_before_hatched >= 100:
			hatched = Adopt.objects.filter(hatch_time__gte=today_start, hatch_time__lte=today_end).count()
			return hatched
		else:
			return 1000.1





