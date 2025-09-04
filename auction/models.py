from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DF', 'Defender'),
        ('MF', 'Midfielder'),
        ('FW', 'Forward'),
    ]
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    playing_style = models.CharField(max_length=100)
    image = models.ImageField(upload_to='players/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    market_value = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    
    def __str__(self):
        return f"{self.name} ({self.position}) - ${self.market_value}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Bid(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-amount']
    
    def __str__(self):
        return f"{self.user.username} - {self.player.name} - ${self.amount}"