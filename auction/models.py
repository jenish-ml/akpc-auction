from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Player(models.Model):
    POSITION_CHOICES = [
        ('CF', 'Center Forwards'),
        ('SS', 'Second Strikers'),
        ('RWF', 'Right Wingers'),
        ('LWF', 'Left Wingers'),
        ('AMF', 'Attacking Midfielders'),
        ('LMF', 'Left Midfielders'),
        ('RMF', 'Right Midfielders'),
        ('CMF', 'Center Midfielders'),
        ('DMF', 'Defensive Midfielders'),
        ('LB', 'Left Backs'),
        ('RB', 'Right Backs'),
        ('CB', 'Center Backs'),
        ('GK', 'Goalkeepers'),
    ]
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    rating = models.CharField(max_length=10, blank=True, null=True, help_text="e.g. 5⭐️")
    playing_style = models.CharField(max_length=100)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    market_value = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    
    def __str__(self):
        return f"{self.name} ({self.position}) - ${self.market_value}"

class Team(models.Model):
    LEAGUE_CHOICES = [
        ('Pro', 'AKPC Pro League'),
        ('Super', 'AKPC Super League'),
        ('Base', 'AKPC Base League'),
        ('Reserve', 'AKPC Reserve League'),
        ('Rookie', 'AKPC Rookie League'),
    ]
    name = models.CharField(max_length=100, unique=True)
    league = models.CharField(max_length=20, choices=LEAGUE_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    def __str__(self):
        return f"{self.name} ({self.get_league_display()}) - ${self.balance}M"

class Transaction(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team.name} - {self.description} : ${self.amount}M"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    team = models.OneToOneField(Team, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Bid(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-amount']
    
    def __str__(self):
        return f"{self.user.username} - {self.player.name} - ${self.amount}"