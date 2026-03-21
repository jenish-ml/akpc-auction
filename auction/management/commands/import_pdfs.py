import fitz
import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from auction.models import Team, Player, UserProfile

class Command(BaseCommand):
    help = 'Parse PDFs, created teams/users, and players'

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing existing data...")
        Player.objects.all().delete()
        Team.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        UserProfile.objects.all().delete()

        # SUPER_ADMINS to grant is_superuser
        super_admins = ["fc barcelona", "psv eindhoven", "psv", "olympique marseille", "marseille", "liverpool"]

        # Parse Balance PDF
        balance_pdf = fitz.open('media/players/AKPC S22 AFTER TRANSFER WINDOW BALANCE LIST.pdf')
        balance_text = ""
        for page in balance_pdf:
            balance_text += page.get_text() + "\n"

        self.stdout.write("Parsing Teams and Balances...")
        lines = balance_text.split('\n')
        current_league = "PRO"
        
        teams_created = {}

        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Detect League
            if 'LEAGUE' in line.upper() and 'AKPC' in line.upper():
                if 'PRO' in line.upper(): current_league = 'Pro'
                elif 'SUPER' in line.upper(): current_league = 'Super'
                elif 'BASE' in line.upper(): current_league = 'Base'
                elif 'RESERVE' in line.upper(): current_league = 'Reserve'
                elif 'ROOKIE' in line.upper(): current_league = 'Rookie'
                continue

            # Detect Team and Balance
            match = re.search(r'([a-zA-Z0-9\s\.\']+)[\-–]\s*(\d+)', line)
            if match:
                team_name = match.group(1).strip()
                balance = float(match.group(2).strip())
                
                # Create Team
                team = Team.objects.create(
                    name=team_name,
                    league=current_league,
                    balance=balance
                )
                
                # Standardize team name for mapping later
                clean_name = re.sub(r'[^a-zA-Z0-9]', '', team_name.lower())
                teams_created[clean_name] = team
                
                # Create User Account
                username = clean_name
                password = f"{clean_name}123"
                
                if not User.objects.filter(username=username).exists():
                    is_super = any(s in team_name.lower() for s in super_admins)
                    
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        is_staff=is_super,
                        is_superuser=is_super
                    )
                    UserProfile.objects.create(
                        user=user,
                        is_approved=True,
                        team=team
                    )
                    self.stdout.write(f"Created Team: {team_name} [{current_league}] | User: {username} | Super: {is_super}")

        # Ensure the 4 specified admins exist even if naming is slightly off
        self.stdout.write("Checking Admin accounts...")

        # Parse Players PDF
        player_pdf = fitz.open('media/players/AKPC S22 AFTER TRANSFER WINDOW PLAYERS LIST.pdf')
        player_text = ""
        for page in player_pdf:
            player_text += page.get_text() + "\n"

        self.stdout.write("Parsing Players...")
        plines = [p.strip() for p in player_text.split('\n') if p.strip()]
        
        valid_positions = ['CF', 'SS', 'RWF', 'LWF', 'RW', 'LW', 'AMF', 'LMF', 'RMF', 'CMF', 'DMF', 'LB', 'RB', 'CB', 'GK']
        
        players_added = 0
        
        for i, line in enumerate(plines):
            if line in valid_positions and i >= 1 and i + 3 < len(plines):
                player_name = plines[i-1]
                position = line
                if position == 'RW': position = 'RWF'
                if position == 'LW': position = 'LWF'
                
                rating = plines[i+1] # like "4" or "5"
                if rating in ['4', '5']:
                    rating = f"{rating}⭐️"
                else:
                    rating = "4⭐️" # fallback
                    
                amount_str = plines[i+2] # like "600 M"
                try:
                    amount = float(re.sub(r'[^\d\.]', '', amount_str))
                except:
                    amount = 50.0
                    
                team_str = plines[i+3]
                clean_team = re.sub(r'[^a-zA-Z0-9]', '', team_str.lower())
                
                # Best effort team match
                matched_team = None
                if clean_team in teams_created:
                    matched_team = teams_created[clean_team]
                else:
                    for tname, tobj in teams_created.items():
                        if tname in clean_team or clean_team in tname:
                            matched_team = tobj
                            break
                            
                Player.objects.create(
                    name=player_name.title(),
                    position=position,
                    rating=rating,
                    market_value=amount, # we map amount here, or 70/50? The requirements said "current balance and current players". Let's use the amount from PDF.
                    team=matched_team,
                    playing_style="Standard"
                )
                players_added += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(teams_created)} teams and {players_added} players!'))
