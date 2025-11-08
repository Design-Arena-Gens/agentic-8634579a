from __future__ import annotations

from django.contrib import admin

from tournaments.models import Team, Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender_category', 'age_bracket', 'start_date', 'end_date', 'registration_open')
    list_filter = ('gender_category', 'age_bracket', 'registration_open')
    search_fields = ('name',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'tournament', 'mentor')
    list_filter = ('tournament',)
    search_fields = ('name', 'mentor')
