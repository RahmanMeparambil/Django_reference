from django.db import models


# Player Model
class Player( models.Model ):
    name = models.CharField( max_length=255 )
    date_of_birth = models.DateField()
    nationality = models.CharField( max_length=100 )
    ranking_points = models.IntegerField( default=0 )

    def __str__(self):
        return self.name


# Tournament Model
class Tournament(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


# Matches Model
class Matches(models.Model):
    ROUND_CHOICES = [
        ('Round of 32', 'Round of 32'),
        ('Round of 16', 'Round of 16'),
        ('Quarter-Final', 'Quarter-Final'),
        ('Semi-Final', 'Semi-Final'),
        ('Final', 'Final'),
    ]
    
    player1 = models.ForeignKey(Player, related_name='matches_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='matches_player2', on_delete=models.CASCADE)
    winner = models.ForeignKey(Player, related_name='matches_winner', null=True, blank=True, on_delete=models.SET_NULL)
    tournament = models.ForeignKey(Tournament, related_name='matches', on_delete=models.CASCADE)
    round = models.CharField(max_length=50, choices=ROUND_CHOICES)
    score = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.player1} vs {self.player2} - {self.round} - {self.tournament}"

