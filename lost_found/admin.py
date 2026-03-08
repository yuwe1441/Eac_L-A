from django.contrib import admin
from .models import Claim, Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'moderation_status', 'category', 'reporter_name', 'date_reported')
    list_filter = ('status', 'moderation_status', 'category')
    search_fields = ('title', 'description', 'location', 'reporter_name', 'reporter_contact')


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('item', 'claimant_name', 'claimant_contact', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('item__title', 'claimant_name', 'claimant_contact', 'reason')