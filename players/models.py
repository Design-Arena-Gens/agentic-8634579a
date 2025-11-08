from __future__ import annotations

import secrets
from datetime import date

from django.db import models


class Player(models.Model):
    GENDER_CHOICES = [
        ('girl', 'Girl'),
        ('boy', 'Boy'),
        ('woman', 'Woman'),
        ('man', 'Man'),
        ('other', 'Other'),
    ]

    PLAYING_POSITIONS = [
        ('goal_shooter', 'Goal Shooter'),
        ('goal_attack', 'Goal Attack'),
        ('wing_attack', 'Wing Attack'),
        ('centre', 'Centre'),
        ('wing_defence', 'Wing Defence'),
        ('goal_defence', 'Goal Defence'),
        ('goal_keeper', 'Goal Keeper'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    playing_position = models.CharField(max_length=50, choices=PLAYING_POSITIONS)
    photo = models.ImageField(upload_to='players/photos/', default='defaults/player_default.png', blank=True)
    institution_name = models.CharField(max_length=255)
    registration_code = models.CharField(max_length=4, unique=True, editable=False)
    tournament = models.ForeignKey('tournaments.Tournament', on_delete=models.SET_NULL, null=True, blank=True)
    consent_to_play = models.BooleanField(default=False)
    team = models.ForeignKey('tournaments.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return f'{self.name} ({self.registration_code})'

    def save(self, *args, **kwargs):
        if not self.registration_code:
            self.registration_code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    age.short_description = 'Age'  # type: ignore[attr-defined]

    @property
    def age_category(self) -> str:
        player_age = self.age()
        if player_age <= 14:
            return 'Under 14'
        if player_age <= 16:
            return 'Under 16'
        if player_age <= 17:
            return 'Under 17'
        if player_age <= 19:
            return 'Under 19'
        return 'Open'

    def _generate_unique_code(self) -> str:
        while True:
            code = f'{secrets.randbelow(10000):04d}'
            if not Player.objects.filter(registration_code=code).exists():
                return code
