from django.contrib import admin
from .models import Pokemon, Adopt, Lab, Interaction, Box, Dex, Hunt, Trade, Contract, PotentialContract, ShinyCharm, DaycareEgg

# Register your models here.
admin.site.register(Pokemon)
admin.site.register(Adopt)
admin.site.register(Lab)
admin.site.register(Interaction)
admin.site.register(Box)
admin.site.register(Dex)
admin.site.register(Hunt)
admin.site.register(Trade)
admin.site.register(Contract)
admin.site.register(PotentialContract)
admin.site.register(ShinyCharm)
admin.site.register(DaycareEgg)