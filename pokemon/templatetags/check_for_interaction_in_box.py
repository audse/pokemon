from django import template
from core.views import check_interaction
from pokedex.models import Adopt

register = template.Library()

@register.assignment_tag
def check_for_interaction_in_box(user, pk):
	if user.is_authenticated():
		adopt = Adopt.objects.filter(pk=pk).first()
		check_interaction(user, adopt)
		return adopt.can_interact
	else:
		adopt = Adopt.objects.filter(pk=pk).first()
		adopt.can_interact = False
		return adopt.can_interact