from django.urls import path

from players import views

urlpatterns = [
    path('', views.home, name='home'),
    path('success/<str:code>/', views.registration_success, name='registration_success'),
    path('lookup/', views.player_lookup, name='player_lookup'),
]
