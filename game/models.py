from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name


class Game(models.Model):
    player_a = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_a')
    player_b = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_b', blank=True)
    current_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='current_player', blank=True)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='winner', blank=True)
    steps = models.CharField(max_length=1000)