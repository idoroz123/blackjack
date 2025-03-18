import datetime
from django.db import models
import uuid

class GameSession(models.Model):
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deck_id = models.CharField(max_length=100)
    player_hand = models.JSONField(default=list)
    dealer_hand = models.JSONField(default=list)
    game_state = models.CharField(max_length=20, default="NOT_STARTED")
    created_at = models.DateTimeField(auto_now_add=True)
    

class GameHistory(models.Model):
    session_id = models.CharField(max_length=255)
    player_hand = models.JSONField()
    dealer_hand = models.JSONField()
    player_score = models.IntegerField()
    dealer_score = models.IntegerField()
    outcome = models.CharField(max_length=50)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Game {self.session_id} - {self.outcome} at {self.timestamp}"