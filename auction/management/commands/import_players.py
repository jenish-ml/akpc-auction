from django.core.management.base import BaseCommand
from auction.models import Player

class Command(BaseCommand):
    help = 'Import players from text list'

    def handle(self, *args, **options):
        players_data = [

            # STRIKERS
            {"name": "KARIM BENZEMA", "position": "FW", "market_value": 70.00},
            {"name": "HARRY KANE", "position": "FW", "market_value": 70.00},
            {"name": "JONATHAN BURKARDT", "position": "FW", "market_value": 50.00},
            {"name": "EVANN GUESSAND", "position": "FW", "market_value": 50.00},
            {"name": "STRAND LARSON", "position": "FW", "market_value": 50.00},
            {"name": "OLIVER GIROUD", "position": "FW", "market_value": 50.00},
            {"name": "NICK WOLTERMADE", "position": "FW", "market_value": 50.00},
            {"name": "OYARZABAL", "position": "FW", "market_value": 50.00},
            {"name": "BUDIMIR", "position": "FW", "market_value": 50.00},
            {"name": "CHRIS WOOD", "position": "FW", "market_value": 50.00},
            {"name": "LUIS SUAREZ", "position": "FW", "market_value": 50.00},
            {"name": "LUCAS BELTRAN", "position": "FW", "market_value": 50.00},
            {"name": "KAIO JORGE", "position": "FW", "market_value": 50.00},

            # SECOND STRIKER
            {"name": "KENAN YILDIZ", "position": "FW", "market_value": 50.00},
            {"name": "THOMAS MULLER", "position": "FW", "market_value": 50.00},
            {"name": "TALISCA", "position": "FW", "market_value": 50.00},

            # LEFT WINGERS
            {"name": "LUIS DIAZ", "position": "FW", "market_value": 70.00},
            {"name": "MATHYS TEL", "position": "FW", "market_value": 50.00},
            {"name": "ANTONIO NUSA", "position": "FW", "market_value": 50.00},
            {"name": "FEDERICO CHIESA", "position": "FW", "market_value": 50.00},
            {"name": "CALLUM HUDSON ODOI", "position": "FW", "market_value": 50.00},
            {"name": "MARTIN TERRIER", "position": "FW", "market_value": 50.00},
            {"name": "KINGSLY COMAN", "position": "FW", "market_value": 50.00},
            {"name": "JACK GREALISH", "position": "FW", "market_value": 50.00},
            {"name": "ALEX IWOBI", "position": "FW", "market_value": 50.00},

            # RIGHT WINGERS
            {"name": "NONI MADUEKE", "position": "FW", "market_value": 70.00},
            {"name": "PHIL FODEN", "position": "FW", "market_value": 70.00},
            {"name": "ANTOINE SEMENYO", "position": "FW", "market_value": 70.00},
            {"name": "LEROY SANE", "position": "FW", "market_value": 50.00},
            {"name": "LUKEBAKIYO", "position": "FW", "market_value": 50.00},
            {"name": "MOUSSA DIABY", "position": "FW", "market_value": 50.00},
            {"name": "QUENDA", "position": "FW", "market_value": 50.00},
            {"name": "ANGEL CORREA", "position": "FW", "market_value": 50.00},
            {"name": "FRANCO MASTANTUONO", "position": "FW", "market_value": 50.00},
            {"name": "EDON ZHEGROVA", "position": "FW", "market_value": 50.00},
            {"name": "POLITANO", "position": "FW", "market_value": 50.00},
            {"name": "ANGEL DI MARIA", "position": "FW", "market_value": 50.00},

            # ATTACKING MIDFIELDERS
            {"name": "BERNARDO SILVA", "position": "MF", "market_value": 70.00},
            {"name": "ARDA GULER", "position": "MF", "market_value": 70.00},
            {"name": "RODRYGO GARRO", "position": "MF", "market_value": 50.00},
            {"name": "MARCO ASENSIO", "position": "MF", "market_value": 50.00},
            {"name": "RYAN CHERKI", "position": "MF", "market_value": 50.00},
            {"name": "PELLEGRINI", "position": "MF", "market_value": 50.00},
            {"name": "G.DE ARRASCAETA", "position": "MF", "market_value": 50.00},
            {"name": "LAZAR SAMARDZIC", "position": "MF", "market_value": 50.00},
            {"name": "ISMAILA SARR", "position": "MF", "market_value": 50.00},
            {"name": "SUDAKOV", "position": "MF", "market_value": 50.00},
            {"name": "RODRIGO MORA", "position": "MF", "market_value": 50.00},
            {"name": "AMINE ADLI", "position": "MF", "market_value": 50.00},
            {"name": "CAN UZUN", "position": "MF", "market_value": 50.00},

            # CENTER MIDFIELDERS
            {"name": "TIJJANI REIJNDERS", "position": "MF", "market_value": 70.00},
            {"name": "LEON GORETZKA", "position": "MF", "market_value": 50.00},
            {"name": "MARCO VERRATTI", "position": "MF", "market_value": 50.00},
            {"name": "JOHN MCGIN", "position": "MF", "market_value": 50.00},
            {"name": "PASCAL GROSS", "position": "MF", "market_value": 50.00},
            {"name": "LUKA MODRIC", "position": "MF", "market_value": 50.00},
            {"name": "GALLAGHER", "position": "MF", "market_value": 50.00},
            {"name": "CURTIS JONES", "position": "MF", "market_value": 50.00},
            {"name": "JOELINTON", "position": "MF", "market_value": 50.00},

            # DEFENSIVE MIDFIELDERS
            {"name": "FABHINO", "position": "MF", "market_value": 50.00},
            {"name": "ANDRE", "position": "MF", "market_value": 50.00},
            {"name": "LEANDRO PAREDES", "position": "MF", "market_value": 50.00},
            {"name": "DOUCOURE", "position": "MF", "market_value": 50.00},
            {"name": "ADAM WHARTON", "position": "MF", "market_value": 50.00},

            # LEFT BACK
            {"name": "ALEJANDRO BALDE", "position": "DF", "market_value": 70.00},
            {"name": "IAN MAATSEN", "position": "DF", "market_value": 50.00},
            {"name": "DAVID RAUM", "position": "DF", "market_value": 50.00},
            {"name": "ROBERTSON", "position": "DF", "market_value": 50.00},
            {"name": "AIT NOURI", "position": "DF", "market_value": 50.00},

            # RIGHT BACK
            {"name": "DI LORENZO", "position": "DF", "market_value": 50.00},
            {"name": "DANILO", "position": "DF", "market_value": 50.00},
            {"name": "DIOGO DALOT", "position": "DF", "market_value": 50.00},

            # CENTER BACK
            {"name": "WILLIAN PACHO", "position": "DF", "market_value": 70.00},
            {"name": "CHRISTHIAN MOSQUERA", "position": "DF", "market_value": 70.00},
            {"name": "MALICK THIAW", "position": "DF", "market_value": 50.00},
            {"name": "EZRI KONSA", "position": "DF", "market_value": 50.00},
            {"name": "LUCAS HERNANDEZ", "position": "DF", "market_value": 50.00},

            # GOALKEEPERS
            {"name": "Y.SOMMER", "position": "GK", "market_value": 70.00},
            {"name": "J.PICKFORD", "position": "GK", "market_value": 50.00},
            {"name": "BENTO", "position": "GK", "market_value": 50.00},
            {"name": "LIVAKOVIC", "position": "GK", "market_value": 50.00},
            {"name": "RAMSDALE", "position": "GK", "market_value": 50.00},
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