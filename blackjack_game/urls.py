from django.urls import path
from . import views

urlpatterns = [
    path('start_game/', views.start_game, name='start_game'),
    path("game_state/<str:session_id>/", views.game_state, name="game_state"),
    path("hit/<str:session_id>/", views.hit, name="hit"),
    path("stand/<str:session_id>/", views.stand, name="stand"),
    path("restart/<str:session_id>/", views.restart_game, name="restart_game"),
    path('history/<str:session_id>/', views.get_game_history, name="get_game_history"),

]
