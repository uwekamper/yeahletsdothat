from django.contrib import admin
from campaigns.models import Campaign

class ActivityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Campaign, ActivityAdmin)