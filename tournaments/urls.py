from django.urls import path

from tournaments import views

urlpatterns = [
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('admin/players/table/', views.player_table, name='player_table'),
    path('admin/tournaments/', views.tournament_list, name='tournament_list'),
    path('admin/teams/', views.team_list, name='team_list'),
    path('admin/players/<int:player_id>/assign-team/', views.assign_player_team, name='assign_player_team'),
]
