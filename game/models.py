from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name


class Game(models.Model):
    player_a = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='own_games')
    player_b = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='other_games', null=True)
    #current_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='current_games', null=True)
    move_a = models.CharField(max_length=10, null=True)
    move_b = models.CharField(max_length=10, null=True)
    winner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='won_games', null=True)
    steps = models.CharField(max_length=1000)