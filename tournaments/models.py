from __future__ import annotations

from django.conf import settings
from django.db import models


class Tournament(models.Model):
    GENDER_CATEGORY_CHOICES = [
        ('girls', 'Girls'),
        ('boys', 'Boys'),
        ('women', 'Women'),
        ('men', 'Men'),
        ('mixed', 'Mixed'),
    ]

    AGE_BRACKET_CHOICES = [
        ('under14', 'Under 14'),
        ('under16', 'Under 16'),
        ('under17', 'Under 17'),
        ('under19', 'Under 19'),
        ('open', 'Open'),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    gender_category = models.CharField(max_length=10, choices=GENDER_CATEGORY_CHOICES, default='mixed')
    age_bracket = models.CharField(max_length=10, choices=AGE_BRACKET_CHOICES, default='open')
    registration_open = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tournaments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='teams/logos/', default='defaults/team_default.png', blank=True)
    mentor = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('tournament', 'name')
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name} - {self.tournament.name}'
