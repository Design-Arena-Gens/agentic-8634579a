from __future__ import annotations

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from players.forms import PlayerRegistrationForm
from players.models import Player


def home(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = PlayerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            player = form.save()
            messages.success(
                request,
                f'Thank you for registering, {player.name}! Your reference number is {player.registration_code}.',
            )
            return redirect(reverse('players:registration_success', kwargs={'code': player.registration_code}))
    else:
        form = PlayerRegistrationForm()

    return render(request, 'players/home.html', {'form': form})


def registration_success(request: HttpRequest, code: str) -> HttpResponse:
    player = get_object_or_404(Player, registration_code=code)
    return render(request, 'players/registration_success.html', {'player': player})


def player_lookup(request: HttpRequest) -> HttpResponse:
    query = request.GET.get('registration_code', '').strip()
    player = None
    if query:
        player = Player.objects.filter(registration_code__iexact=query).select_related('tournament', 'team').first()
        if not player:
            messages.error(request, 'No player found with that reference number.')

    template = 'players/partials/lookup_result.html' if request.htmx else 'players/player_lookup.html'
    context = {'player': player, 'query': query}
    return render(request, template, context)
