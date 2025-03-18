from django.urls import path
from . import views

urlpatterns = [
    path('start_game/', views.start_game, name='start_game'),
    path("game_state/<uuid:session_id>/", views.game_state, name="game_state"),
    path("hit/<uuid:session_id>/", views.hit, name="hit"),
    path("stand/<uuid:session_id>/", views.stand, name="stand"),
    path("restart/<uuid:session_id>/", views.restart_game, name="restart_game"),
]
