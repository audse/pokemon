from django.contrib import admin
from .models import Pokemon, Adopt, Lab, Interaction, Box, Dex

# Register your models here.
admin.site.register(Pokemon)
admin.site.register(Adopt)
admin.site.register(Lab)
admin.site.register(Interaction)
admin.site.register(Box)
admin.site.register(Dex)