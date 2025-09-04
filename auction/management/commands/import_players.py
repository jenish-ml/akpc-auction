from django.core.management.base import BaseCommand
from auction.models import Player

class Command(BaseCommand):
    help = 'Import players from text list'

    def handle(self, *args, **options):
        players_data = [
            # STRIKERS
            {"name": "HARRY KANE", "position": "FW", "market_value": 70.00},
            {"name": "SERHOU GUIRASSY", "position": "FW", "market_value": 70.00},
            {"name": "HUGO EKITIKE", "position": "FW", "market_value": 70.00},
            {"name": "ALEXANDER SORLOTH", "position": "FW", "market_value": 50.00},
            {"name": "M.DEPAY", "position": "FW", "market_value": 50.00},
            {"name": "PAVILIDIS", "position": "FW", "market_value": 50.00},
            {"name": "RICHARLISON", "position": "FW", "market_value": 50.00},
            {"name": "PATRICK SCHICK", "position": "FW", "market_value": 50.00},
            {"name": "GABRIEL JESUS", "position": "FW", "market_value": 50.00},
            {"name": "MAXIMILIAN BEIER", "position": "FW", "market_value": 50.00},
            {"name": "VICTOR ROQUE", "position": "FW", "market_value": 50.00},
            {"name": "OYARZABAL", "position": "FW", "market_value": 50.00},
            {"name": "THIERNO BARRY", "position": "FW", "market_value": 50.00},
            {"name": "GIANLUCA SCAMACCA", "position": "FW", "market_value": 50.00},
            {"name": "AUBAMEYANG", "position": "FW", "market_value": 50.00},
            {"name": "BETO", "position": "FW", "market_value": 50.00},
            {"name": "YURI ALBERTO", "position": "FW", "market_value": 50.00},
            {"name": "LUCAS BELTRAN", "position": "FW", "market_value": 50.00},
            
            # SECOND STRIKER
            {"name": "RAFA SILVA", "position": "FW", "market_value": 50.00},
            {"name": "KENAN YILDIZ", "position": "FW", "market_value": 50.00},
            
            # LEFT WINGERS
            {"name": "RAFAEL LEAO", "position": "FW", "market_value": 70.00},
            {"name": "MATTIA ZACCAGNI", "position": "FW", "market_value": 50.00},
            {"name": "GARNACHO", "position": "FW", "market_value": 50.00},
            {"name": "KEVIN SCHADE", "position": "FW", "market_value": 50.00},
            {"name": "SADIO MANE", "position": "FW", "market_value": 50.00},
            {"name": "ANTONIO NUSA", "position": "FW", "market_value": 50.00},
            {"name": "ALBERT MOLEIRO", "position": "FW", "market_value": 50.00},
            {"name": "JAMMIE GITTENS", "position": "FW", "market_value": 50.00},
            {"name": "IGOR PAIXAO", "position": "FW", "market_value": 50.00},
            {"name": "CALLUM HUDSON ODOI", "position": "FW", "market_value": 50.00},
            
            # RIGHT WINGERS
            {"name": "MASON GREENWOOD", "position": "FW", "market_value": 70.00},
            {"name": "PEDRO NETO", "position": "FW", "market_value": 50.00},
            {"name": "FRANCISCO TRINCAO", "position": "FW", "market_value": 50.00},
            {"name": "DAVID NERES", "position": "FW", "market_value": 50.00},
            {"name": "ESTEVAO", "position": "FW", "market_value": 50.00},
            {"name": "KARIM ADAYEMI", "position": "FW", "market_value": 50.00},
            {"name": "ANTONY", "position": "FW", "market_value": 50.00},
            {"name": "FRANCO MASTANTUONO", "position": "FW", "market_value": 50.00},
            {"name": "MALCOM", "position": "FW", "market_value": 50.00},
            {"name": "AMAD DIALLO", "position": "FW", "market_value": 50.00},
            
            # ATTACKING MIDFIELDERS
            {"name": "MORGAN ROGERS", "position": "MF", "market_value": 70.00},
            {"name": "BERNARDO SILVA", "position": "MF", "market_value": 70.00},
            {"name": "JULIAN BRANDT", "position": "MF", "market_value": 50.00},
            {"name": "JAMES MADISSON", "position": "MF", "market_value": 50.00},
            {"name": "ISCO", "position": "MF", "market_value": 50.00},
            {"name": "AMINE ADLI", "position": "MF", "market_value": 50.00},
            {"name": "PELLEGRINI", "position": "MF", "market_value": 50.00},
            {"name": "RAYAN CHERKI", "position": "MF", "market_value": 50.00},
            {"name": "NKUNKU", "position": "MF", "market_value": 50.00},
            {"name": "LAZAR SAMARDZIC", "position": "MF", "market_value": 50.00},
            {"name": "GIOVANI LO CELSO", "position": "MF", "market_value": 50.00},
            {"name": "MIKEL DAMSGAARD", "position": "MF", "market_value": 50.00},
            
            # LEFT MIDFIELDERS
            {"name": "JACOB RAMSEY", "position": "MF", "market_value": 50.00},
            {"name": "MOHAMMED KUDUS", "position": "MF", "market_value": 50.00},
            
            # RIGHT MIDFIELDERS
            {"name": "GIULIANO SIMEONE", "position": "MF", "market_value": 50.00},
            {"name": "DENZEL DUMFRIES", "position": "MF", "market_value": 50.00},
            {"name": "SIMON ADINGRA", "position": "MF", "market_value": 50.00},
            {"name": "LUIS ENRIQUE", "position": "MF", "market_value": 50.00},
            {"name": "JUAN CUADRADO", "position": "MF", "market_value": 50.00},
            
            # CENTER MIDFIELDERS
            {"name": "TIJJANI REIJNDERS", "position": "MF", "market_value": 70.00},
            {"name": "WARREN ZAIRE EMERY", "position": "MF", "market_value": 70.00},
            {"name": "PASCAL GROSS", "position": "MF", "market_value": 50.00},
            {"name": "S.MILINKOVIC SAVIC", "position": "MF", "market_value": 50.00},
            {"name": "PAUL POGBA", "position": "MF", "market_value": 50.00},
            {"name": "ZIELENSKI", "position": "MF", "market_value": 50.00},
            {"name": "MATHEUS NUNES", "position": "MF", "market_value": 50.00},
            {"name": "JOHN MCGIN", "position": "MF", "market_value": 50.00},
            {"name": "CURTIS JONES", "position": "MF", "market_value": 50.00},
            {"name": "PABLO BARRIOS", "position": "MF", "market_value": 50.00},
            {"name": "MCKENNIE", "position": "MF", "market_value": 50.00},
            {"name": "NICOLAS DOMINGUEZ", "position": "MF", "market_value": 50.00},
            
            # DEFENSIVE MIDFIELDERS
            {"name": "TCHOUAMENI", "position": "MF", "market_value": 70.00},
            {"name": "BRUNO GUIMARAES", "position": "MF", "market_value": 50.00},
            {"name": "JOAO PALINHA", "position": "MF", "market_value": 50.00},
            {"name": "RUBEN NEVES", "position": "MF", "market_value": 50.00},
            {"name": "THOMAS PARTEY", "position": "MF", "market_value": 50.00},
            {"name": "MARCELO BROZOVIC", "position": "MF", "market_value": 50.00},
            {"name": "SCOTT MCTOMINY", "position": "MF", "market_value": 50.00},
            {"name": "MARC CASADO", "position": "MF", "market_value": 50.00},
            {"name": "FELIX NMECHA", "position": "MF", "market_value": 50.00},
            {"name": "ANDRE", "position": "MF", "market_value": 50.00},
            
            # LEFT BACK
            {"name": "DESTINY UDOGIE", "position": "DF", "market_value": 70.00},
            {"name": "THEO HERNANDEZ", "position": "DF", "market_value": 70.00},
            {"name": "ALEJANDRO BALDE", "position": "DF", "market_value": 70.00},
            {"name": "DAVID RAUM", "position": "DF", "market_value": 50.00},
            {"name": "MYLES LEWIS-SKELLY", "position": "DF", "market_value": 50.00},
            {"name": "IAN MAATSEN", "position": "DF", "market_value": 50.00},
            {"name": "RAYAN AIT-NOURI", "position": "DF", "market_value": 50.00},
            {"name": "MILOS KERKEZ", "position": "DF", "market_value": 50.00},
            
            # RIGHT BACK
            {"name": "JURRIEN TIMBER", "position": "DF", "market_value": 70.00},
            {"name": "RAOUL BELLANOVA", "position": "DF", "market_value": 50.00},
            {"name": "DANILO", "position": "DF", "market_value": 50.00},
            {"name": "PEDRO PORRO", "position": "DF", "market_value": 50.00},
            {"name": "GONZALO MONTIEL", "position": "DF", "market_value": 50.00},
            {"name": "DJED SPENCE", "position": "DF", "market_value": 50.00},
            {"name": "OLA AINA", "position": "DF", "market_value": 50.00},
            {"name": "YAN COUTO", "position": "DF", "market_value": 50.00},
            
            # CENTER BACK
            {"name": "DEAN HUIJSEN", "position": "DF", "market_value": 70.00},
            {"name": "WALDEMAR ANTON", "position": "DF", "market_value": 50.00},
            {"name": "GIORGIO SCALVINI", "position": "DF", "market_value": 50.00},
            {"name": "L.HENRANDEZ", "position": "DF", "market_value": 50.00},
            {"name": "WILLI ORBAN", "position": "DF", "market_value": 50.00},
            {"name": "NIKOLA MILENKOVIC", "position": "DF", "market_value": 50.00},
            {"name": "VAN HACKE", "position": "DF", "market_value": 50.00},
            {"name": "A.BUONGIORNO", "position": "DF", "market_value": 50.00},
            {"name": "JARRAD BRANTHWAITE", "position": "DF", "market_value": 50.00},
            {"name": "RAUL ASENSIO", "position": "DF", "market_value": 50.00},
            {"name": "PIERRE KALULU", "position": "DF", "market_value": 50.00},
            {"name": "FABIAN SCHAR", "position": "DF", "market_value": 50.00},
            {"name": "HINCAPIE", "position": "DF", "market_value": 50.00},
            {"name": "ABDUKODIR KHUSANOV", "position": "DF", "market_value": 50.00},
            {"name": "BENJAMIN PAVARD", "position": "DF", "market_value": 50.00},
            {"name": "NICOLAS OTAMENDI", "position": "DF", "market_value": 50.00},
            {"name": "BERALDO", "position": "DF", "market_value": 50.00},
            {"name": "ARCHIE GRAY", "position": "DF", "market_value": 50.00},
            
            # GOALKEEPERS
            {"name": "JOAN GARCIA", "position": "GK", "market_value": 70.00},
            {"name": "ALVARO VALLES", "position": "GK", "market_value": 50.00},
            {"name": "ALEXANDER NUBEL", "position": "GK", "market_value": 50.00},
            {"name": "HRADECKY", "position": "GK", "market_value": 50.00},
            {"name": "OLIVER BAUMANN", "position": "GK", "market_value": 50.00},
            {"name": "GREGORIO", "position": "GK", "market_value": 50.00},
            {"name": "V.MILINKOVIC SAVIC", "position": "GK", "market_value": 50.00},
            {"name": "DOMINIK LIVAKOVIC", "position": "GK", "market_value": 50.00},
            {"name": "BENTO", "position": "GK", "market_value": 50.00},
            {"name": "DORDE PETROVIC", "position": "GK", "market_value": 50.00},
        ]

        count = 0
        for player_data in players_data:
            player, created = Player.objects.get_or_create(
                name=player_data["name"],
                defaults={
                    "position": player_data["position"],
                    "market_value": player_data["market_value"],
                    "playing_style": "Standard"
                }
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} players'))