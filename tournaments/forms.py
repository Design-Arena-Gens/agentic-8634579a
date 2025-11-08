from __future__ import annotations

from django import forms

from tournaments.models import Team, Tournament


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = [
            'name',
            'description',
            'start_date',
            'end_date',
            'gender_category',
            'age_bracket',
            'registration_open',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tournament Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender_category': forms.Select(attrs={'class': 'form-select'}),
            'age_bracket': forms.Select(attrs={'class': 'form-select'}),
            'registration_open': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['tournament', 'name', 'logo', 'mentor', 'notes']
        widgets = {
            'tournament': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team Name'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'mentor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Team Mentor'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PlayerTeamAssignmentForm(forms.Form):
    team = forms.ModelChoiceField(
        queryset=Team.objects.none(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
        empty_label='Unassigned',
    )

    def __init__(self, *args, **kwargs):
        tournament = kwargs.pop('tournament', None)
        super().__init__(*args, **kwargs)
        queryset = Team.objects.all()
        if tournament:
            queryset = queryset.filter(tournament=tournament)
        self.fields['team'].queryset = queryset.order_by('name')
