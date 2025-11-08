from __future__ import annotations

from django import forms

from players.models import Player
from tournaments.models import Tournament


class PlayerRegistrationForm(forms.ModelForm):
    consent_to_play = forms.BooleanField(
        required=True,
        label='I agree to participate in the selected tournament',
    )

    class Meta:
        model = Player
        fields = [
            'name',
            'date_of_birth',
            'gender',
            'playing_position',
            'photo',
            'institution_name',
            'tournament',
            'consent_to_play',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'playing_position': forms.Select(attrs={'class': 'form-select'}),
            'institution_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institution / Village'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'tournament': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        open_tournaments = Tournament.objects.filter(registration_open=True).order_by('name')
        self.fields['tournament'].queryset = open_tournaments
        self.fields['tournament'].empty_label = 'Select a tournament'
        self.fields['tournament'].required = open_tournaments.exists()
        self.fields['photo'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit: bool = True):
        self.instance.consent_to_play = self.cleaned_data.get('consent_to_play', False)
        return super().save(commit=commit)
