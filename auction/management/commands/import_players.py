from django.core.management.base import BaseCommand
from auction.models import Player

class Command(BaseCommand):
    help = 'Import players from text list'

    def handle(self, *args, **options):
        players_data = [
            # STRIKERS
            {"name": "Karim Benzema", "position": "ST", "market_value": 70},
            {"name": "Harry Kane", "position": "ST", "market_value": 70},
            {"name": "Jonathan Burkardt", "position": "ST", "market_value": 50},
            {"name": "Evann Guessand", "position": "ST", "market_value": 50},
            {"name": "Strand Larson", "position": "ST", "market_value": 50},
            {"name": "Oliver Giroud", "position": "ST", "market_value": 50},
            {"name": "Nick Woltemade", "position": "ST", "market_value": 50},
            {"name": "Oyarzabal", "position": "ST", "market_value": 50},
            {"name": "Budimir", "position": "ST", "market_value": 50},
            {"name": "Chris Wood", "position": "ST", "market_value": 50},
            {"name": "Luis Suarez", "position": "ST", "market_value": 50},
            {"name": "Lucas Beltran", "position": "ST", "market_value": 50},
            {"name": "Kaio Jorge", "position": "ST", "market_value": 50},

            # SECOND STRIKERS
            {"name": "Kenan Yildiz", "position": "SS", "market_value": 50},
            {"name": "Thomas Muller", "position": "SS", "market_value": 50},
            {"name": "Talisca", "position": "SS", "market_value": 50},

            # LEFT WINGERS
            {"name": "Luis Diaz", "position": "LW", "market_value": 70},
            {"name": "Mathys Tel", "position": "LW", "market_value": 50},
            {"name": "Antonio Nusa", "position": "LW", "market_value": 50},
            {"name": "Federico Chiesa", "position": "LW", "market_value": 50},
            {"name": "Callum Hudson-Odoi", "position": "LW", "market_value": 50},
            {"name": "Martin Terrier", "position": "LW", "market_value": 50},
            {"name": "Kingsley Coman", "position": "LW", "market_value": 50},
            {"name": "Jack Grealish", "position": "LW", "market_value": 50},
            {"name": "Alex Iwobi", "position": "LW", "market_value": 50},

            # RIGHT WINGERS
            {"name": "Noni Madueke", "position": "RW", "market_value": 70},
            {"name": "Phil Foden", "position": "RW", "market_value": 70},
            {"name": "Antoine Semenyo", "position": "RW", "market_value": 70},
            {"name": "Leroy Sane", "position": "RW", "market_value": 50},
            {"name": "Lukebakiyo", "position": "RW", "market_value": 50},
            {"name": "Moussa Diaby", "position": "RW", "market_value": 50},
            {"name": "Quenda", "position": "RW", "market_value": 50},
            {"name": "Angel Correa", "position": "RW", "market_value": 50},
            {"name": "Franco Mastantuono", "position": "RW", "market_value": 50},
            {"name": "Edon Zhegrova", "position": "RW", "market_value": 50},
            {"name": "Politano", "position": "RW", "market_value": 50},
            {"name": "Angel Di Maria", "position": "RW", "market_value": 50},

            # LEFT MIDFIELDERS
            {"name": "Alex Baena", "position": "LM", "market_value": 70},
            {"name": "Samuel Lino", "position": "LM", "market_value": 50},
            {"name": "Malick Fofana", "position": "LM", "market_value": 50},

            # RIGHT MIDFIELDERS
            {"name": "Maghnes Akliouche", "position": "RM", "market_value": 50},

            # ATTACKING MIDFIELDERS
            {"name": "Bernardo Silva", "position": "CAM", "market_value": 70},
            {"name": "Arda Guler", "position": "CAM", "market_value": 70},
            {"name": "Rodrygo Garro", "position": "CAM", "market_value": 50},
            {"name": "Marco Asensio", "position": "CAM", "market_value": 50},
            {"name": "Ryan Cherki", "position": "CAM", "market_value": 50},
            {"name": "Pellegrini", "position": "CAM", "market_value": 50},
            {"name": "G. de Arrascaeta", "position": "CAM", "market_value": 50},
            {"name": "Lazar Samardzic", "position": "CAM", "market_value": 50},
            {"name": "Ismaila Sarr", "position": "CAM", "market_value": 50},
            {"name": "Sudakov", "position": "CAM", "market_value": 50},
            {"name": "Rodrigo Mora", "position": "CAM", "market_value": 50},
            {"name": "Amine Adli", "position": "CAM", "market_value": 50},
            {"name": "Can Uzun", "position": "CAM", "market_value": 50},

            # CENTER MIDFIELDERS
            {"name": "Tijjani Reijnders", "position": "CM", "market_value": 70},
            {"name": "Leon Goretzka", "position": "CM", "market_value": 50},
            {"name": "Marco Verratti", "position": "CM", "market_value": 50},
            {"name": "John McGinn", "position": "CM", "market_value": 50},
            {"name": "Pascal Gross", "position": "CM", "market_value": 50},
            {"name": "Luka Modric", "position": "CM", "market_value": 50},
            {"name": "Gallagher", "position": "CM", "market_value": 50},
            {"name": "Elliot Anderson", "position": "CM", "market_value": 50},
            {"name": "Curtis Jones", "position": "CM", "market_value": 50},
            {"name": "Hugo Larsson", "position": "CM", "market_value": 50},
            {"name": "Alex Garcia", "position": "CM", "market_value": 50},
            {"name": "Quinten Timber", "position": "CM", "market_value": 50},
            {"name": "Andrey Santos", "position": "CM", "market_value": 50},
            {"name": "Joelinton", "position": "CM", "market_value": 50},

            # DEFENSIVE MIDFIELDERS
            {"name": "Nico Gonzalez", "position": "CDM", "market_value": 50},
            {"name": "Felix Nmecha", "position": "CDM", "market_value": 50},
            {"name": "Ezequiel Fernandez", "position": "CDM", "market_value": 50},
            {"name": "Fabinho", "position": "CDM", "market_value": 50},
            {"name": "Andre", "position": "CDM", "market_value": 50},
            {"name": "Leandro Paredes", "position": "CDM", "market_value": 50},
            {"name": "Marc Casado", "position": "CDM", "market_value": 50},
            {"name": "Doucoure", "position": "CDM", "market_value": 50},
            {"name": "Carlos Baleba", "position": "CDM", "market_value": 50},
            {"name": "Adam Wharton", "position": "CDM", "market_value": 50},

            # LEFT BACKS
            {"name": "Alejandro Balde", "position": "LB", "market_value": 70},
            {"name": "Ian Maatsen", "position": "LB", "market_value": 50},
            {"name": "David Raum", "position": "LB", "market_value": 50},
            {"name": "Robertson", "position": "LB", "market_value": 50},
            {"name": "Lewis Hall", "position": "LB", "market_value": 50},
            {"name": "Jorrel Hato", "position": "LB", "market_value": 50},
            {"name": "Jose Gaya", "position": "LB", "market_value": 50},
            {"name": "Ait Nouri", "position": "LB", "market_value": 50},

            # RIGHT BACKS
            {"name": "Di Lorenzo", "position": "RB", "market_value": 50},
            {"name": "Danilo", "position": "RB", "market_value": 50},
            {"name": "Diogo Dalot", "position": "RB", "market_value": 50},
            {"name": "Emerson Royal", "position": "RB", "market_value": 50},
            {"name": "Wesley", "position": "RB", "market_value": 50},
            {"name": "Vanderson", "position": "RB", "market_value": 50},
            {"name": "Joaquin Garcia", "position": "RB", "market_value": 50},

            # CENTER BACKS
            {"name": "Willian Pacho", "position": "CB", "market_value": 70},
            {"name": "Christian Mosquera", "position": "CB", "market_value": 70},
            {"name": "Malick Thiaw", "position": "CB", "market_value": 50},
            {"name": "Milenkovic", "position": "CB", "market_value": 50},
            {"name": "Raul Asensio", "position": "CB", "market_value": 50},
            {"name": "Arthur Theate", "position": "CB", "market_value": 50},
            {"name": "Hiroki Ito", "position": "CB", "market_value": 50},
            {"name": "Naif Aguerd", "position": "CB", "market_value": 50},
            {"name": "Christensen", "position": "CB", "market_value": 50},
            {"name": "Leonardo Balerdi", "position": "CB", "market_value": 50},
            {"name": "Mancini", "position": "CB", "market_value": 50},
            {"name": "Danso", "position": "CB", "market_value": 50},
            {"name": "Trevoh Chalobah", "position": "CB", "market_value": 50},
            {"name": "Inigo Martinez", "position": "CB", "market_value": 50},
            {"name": "Ezri Konsa", "position": "CB", "market_value": 50},
            {"name": "Lucas Hernandez", "position": "CB", "market_value": 50},
            {"name": "Goncalo Inacio", "position": "CB", "market_value": 50},
            {"name": "Schuurs", "position": "CB", "market_value": 50},

            # GOALKEEPERS
            {"name": "Y. Sommer", "position": "GK", "market_value": 70},
            {"name": "J. Pickford", "position": "GK", "market_value": 50},
            {"name": "Rajkovic", "position": "GK", "market_value": 50},
            {"name": "James Trafford", "position": "GK", "market_value": 50},
            {"name": "Bento", "position": "GK", "market_value": 50},
            {"name": "V. Milinkovic-Savic", "position": "GK", "market_value": 50},
            {"name": "Alex Meret", "position": "GK", "market_value": 50},
            {"name": "Livakovic", "position": "GK", "market_value": 50},
            {"name": "Kelleher", "position": "GK", "market_value": 50},
            {"name": "Matz Sels", "position": "GK", "market_value": 50},
            {"name": "Ramsdale", "position": "GK", "market_value": 50},
            {"name": "Bernd Leno", "position": "GK", "market_value": 50},
        ]


        count = 0
        for player_data in players_data:
            player, created = Player.objects.get_or_create(
                name=player_data["name"],
                defaults={
                    "position": player_data["position"],
                    "market_value": player_data["market_value"],
                    "playing_style": "Standard",
                }
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} players'))