from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from players.models import Player
from tournaments.forms import PlayerTeamAssignmentForm, TeamForm, TournamentForm
from tournaments.models import Team, Tournament


def admin_login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('tournaments:dashboard')

    form = AuthenticationForm(request, data=request.POST or None)
    form.fields['username'].widget.attrs.update({'class': 'form-control'})
    form.fields['password'].widget.attrs.update({'class': 'form-control'})
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )
        if user is not None:
            login(request, user)
            return redirect('tournaments:dashboard')
        messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'tournaments/admin_login.html', {'form': form})


@login_required
def admin_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('tournaments:admin_login')


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    tournaments = Tournament.objects.order_by('name')
    teams = Team.objects.select_related('tournament').order_by('name')
    context = {
        'tournaments': tournaments,
        'teams': teams,
    }
    return render(request, 'tournaments/dashboard.html', context)


@login_required
def player_table(request: HttpRequest) -> HttpResponse:
    age_filter = request.GET.get('age', 'all')
    gender_filter = request.GET.get('gender', 'all')
    tournament_id = request.GET.get('tournament', '').strip()

    players = Player.objects.select_related('tournament', 'team').order_by('-created_at')

    if age_filter != 'all':
        players = [player for player in players if player.age_category.lower().replace(' ', '') == age_filter]
    else:
        players = list(players)

    if gender_filter != 'all':
        players = [player for player in players if player.gender == gender_filter]

    if tournament_id:
        players = [player for player in players if player.tournament and str(player.tournament_id) == tournament_id]

    for player in players:
        player.current_age = player.age()

    context = {
        'players': players,
    }
    return render(request, 'tournaments/partials/player_table.html', context)


@login_required
def tournament_list(request: HttpRequest) -> HttpResponse:
    tournaments = Tournament.objects.order_by('-created_at')
    form = TournamentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        tournament = form.save(commit=False)
        tournament.created_by = request.user
        tournament.save()
        messages.success(request, 'Tournament created successfully.')
        return redirect('tournaments:tournament_list')

    return render(
        request,
        'tournaments/tournament_list.html',
        {
            'tournaments': tournaments,
            'form': form,
        },
    )


@login_required
def team_list(request: HttpRequest) -> HttpResponse:
    teams = Team.objects.select_related('tournament').order_by('tournament__name', 'name')
    form = TeamForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        team = form.save()
        messages.success(request, f'Team "{team.name}" created.')
        return redirect('tournaments:team_list')
    return render(
        request,
        'tournaments/team_list.html',
        {
            'teams': teams,
            'form': form,
        },
    )


@login_required
def assign_player_team(request: HttpRequest, player_id: int) -> HttpResponse:
    player = get_object_or_404(Player, pk=player_id)

    form = PlayerTeamAssignmentForm(
        request.POST or None,
        tournament=player.tournament,
        initial={'team': player.team},
    )

    if request.method == 'POST' and form.is_valid():
        player.team = form.cleaned_data['team']
        player.save(update_fields=['team'])
        player.current_age = player.age()
        messages.success(request, f'{player.name} team assignment updated.')
        response_template = 'tournaments/partials/player_row.html'
        context = {'player': player, 'show_assignment': True}
        return render(request, response_template, context)

    return render(request, 'tournaments/partials/team_assignment_form.html', {'form': form, 'player': player})
