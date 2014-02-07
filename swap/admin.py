from django.contrib import admin
from swap.models import UserProfile, SeedType, Inventory, Item

admin.site.register(UserProfile)
admin.site.register(SeedType)
admin.site.register(Inventory)
admin.site.register(Item)
