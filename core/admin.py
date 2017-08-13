from django.contrib import admin
from .models import Action, Item, Inventory, Currency, About

# Register your models here.
admin.site.register(Action)
admin.site.register(Item)
admin.site.register(Inventory)
admin.site.register(Currency)
admin.site.register(About)