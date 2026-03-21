import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'efootball_auction.settings')
django.setup()

from auction.models import Team, Player, Transaction, UserProfile
from django.contrib.auth.models import User

# Rename Teams
try:
    psg = Team.objects.filter(name__icontains='germain').first()
    if not psg:
        psg = Team.objects.filter(name__icontains='psg').first()
        
    if psg:
        psg.name = 'PSG (Paris Saint-Germain)'
        psg.save()
        print("Set team name to PSG (Paris Saint-Germain)")
        
        # Check UserProfile for parisfc
        u = User.objects.filter(username='parisfc').first()
        if u and hasattr(u, 'userprofile'):
            u.userprofile.team = psg
            u.userprofile.save()
    else:
        print("Error: Could not find team Germain or PSG.")
except Exception as e:
    print("PSG error:", e)

try:
    rennes = Team.objects.filter(name__icontains='rennai').first()
    if not rennes:
        rennes = Team.objects.filter(name__icontains='rennes').first()
        
    if rennes:
        rennes.name = 'RENNES FC'
        rennes.save()
        print("Set team name to RENNES FC")
except Exception as e:
    print("Rennes error:", e)

psg_players = [
    ("KOKE", "DMF", "4⭐️", 50),
    ("RAPHINHA", "RWF", "5⭐️", 500),
    ("GNABRY", "RWF", "4⭐️", 80),
    ("JACUB KIWIOR", "CB", "4⭐️", 80),
    ("ABDUKODIR KHUSANOV", "CB", "4⭐️", 490),
    ("NICK WOLTERMADE", "CF", "4⭐️", 250),
    ("CURTIS JONES", "CMF", "4⭐️", 150),
    ("N. POPE", "GK", "4⭐️", 250),
]

rennes_players = [
    ("M.DEPAY", "CF", "4⭐️", 180),
    ("KEVIN SCHADE", "LWF", "4⭐️", 290),
    ("FABIAN SCHAR", "CB", "4⭐️", 110),
    ("ALEX MERET", "GK", "4⭐️", 60),
    ("HUGO LARSSON", "CMF", "4⭐️", 100),
    ("WESLEY", "RB", "4⭐️", 60),
]

def assign_players(team, player_data):
    if not team: return
    for name, pos, rating, value in player_data:
        # Check if player exists
        player = Player.objects.filter(name__iexact=name).first()
        if not player:
            player = Player.objects.filter(name__icontains=name.split()[-1]).first()
        
        if not player:
            # Create player if completely missing
            player = Player(name=name, position=pos, rating=rating, base_price=value)
            print(f"Created new player: {name}")
            
        # Update details to match exactly
        player.position = pos
        player.rating = rating
        player.team = team
        # If the model has market_value, I'll set base_price just as a fallback
        if hasattr(player, 'market_value'):
            player.market_value = value
        player.save()
        
        print(f"Assigned {name} to {team.name} for {value}M")

assign_players(psg, psg_players)
assign_players(rennes, rennes_players)

print("Data repair complete.")
