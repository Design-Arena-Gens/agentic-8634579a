from __future__ import annotations

from django.contrib import admin

from players.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'registration_code',
        'gender',
        'playing_position',
        'tournament',
        'team',
        'consent_to_play',
        'age',
    )
    list_filter = ('gender', 'playing_position', 'tournament', 'team', 'consent_to_play')
    search_fields = ('name', 'registration_code', 'institution_name')
