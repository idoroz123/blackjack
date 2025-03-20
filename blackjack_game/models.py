import datetime
import secrets
from django.db import models
import uuid

def generate_session_id():
    return secrets.token_urlsafe(8) 

class GameSession(models.Model):
    session_id = models.CharField(primary_key=True, max_length=16, default=generate_session_id, editable=False, unique=True)
    deck_id = models.CharField(max_length=100)
    player_hand = models.JSONField(default=list)
    dealer_hand = models.JSONField(default=list)
    game_state = models.CharField(max_length=20, default="NOT_STARTED")
    created_at = models.DateTimeField(auto_now_add=True)
    

class GameHistory(models.Model):
    session_id = models.CharField(max_length=16)
    player_hand = models.JSONField()
    dealer_hand = models.JSONField()
    player_score = models.IntegerField()
    dealer_score = models.IntegerField()
    outcome = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Game {self.session_id} - {self.outcome} at {self.timestamp}"