from django.template import Library

from django.utils import timezone
from datetime import datetime, timedelta
from core.models import Action

register = Library()

@register.filter(name="users_online")
def users_online(value):
    online = value
    online -= 1
    time_threshold = datetime.now() - timedelta(minutes=10)
    online = Action.objects.filter(time__gte=time_threshold).filter(online=True).count()
    return online