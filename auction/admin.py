from django.contrib import admin
from .models import Player, UserProfile, Bid

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'market_value', 'playing_style']
    list_filter = ['position', 'market_value']
    search_fields = ['name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_approved', 'created_at']
    list_filter = ['is_approved']
    search_fields = ['user__username']
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
    approve_users.short_description = "Approve selected users"

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['player', 'user', 'amount', 'created_at']
    list_filter = ['player', 'user']
    search_fields = ['player__name', 'user__username']