from django.contrib import admin
from campaigns.models import Campaign, Perk


class PerkInline(admin.StackedInline):
    model = Perk

class CampaignAdmin(admin.ModelAdmin):
    inlines = [PerkInline, ]

admin.site.register(Campaign, CampaignAdmin)
# admin.site.register(Perk, PerkAdmin)