from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Player, Bid

class CustomUserCreationForm(UserCreationForm):
    # Removed the email field
    
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'position', 'market_value', 'playing_style', 'image']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'})
        }