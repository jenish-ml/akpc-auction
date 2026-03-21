from django.core.management.base import BaseCommand
from auction.models import Player

class Command(BaseCommand):
    help = 'Seeds unassigned players into the database for the auction.'

    def handle(self, *args, **kwargs):
        player_data = {
            'CF': {
                '5⭐️': ['KARIM BENZEMA'],
                '4⭐️': ['AYOZE PEREZ', 'JOSELU', 'RICHARLISON', 'SCAMACCA', 'GERARD MORENO', 'O.GIROUD', 'IAGO ASPAS', 'BUDIMIR', 'VICTOR ROQUE', 'DOVBYK', 'IGOR THIAGO', 'TATY CASTELLANOS', 'EMANUEL EMEGHA', 'BRIAN BROBBEY']
            },
            'SS': {
                '4⭐️': ['TALISCA', 'G.RUTTER', 'NKUNKU', 'ADEMOLA LOOKMAN', 'GRIEZMANN']
            },
            'RWF': {
                '4⭐️': ['POLITANO', 'RIYAD MAHREZ', 'ESTEVAO', 'ANTONY', 'RAYAN', 'M.DIABY', 'MATIAS SOULE', 'RICCARDO ORSOLINI', 'NICOLAS GONZALEZ', 'SANCHO']
            },
            'LWF': {
                '4⭐️': ['HUDSON ODOI', 'LORENZO INSIGNE', 'MATHYS TEL', 'GARNACHO', 'SUMMERVILLE', 'DANGO OUATTARA', 'IGOR PAIXAO', 'ALBERTO MOLEIRO']
            },
            'AMF': {
                '5⭐️': ['ARDA GULER'],
                '4⭐️': ['MARCO REUS', 'DAMSGAARD', 'H.AOUAR', 'AIMOR OROZ', 'NICO PAZ', 'MASON MOUNT', 'ZANIOLO', 'GABRI VEIGA', 'ALAN LESCANO', 'ENZO MILLOT']
            },
            'LMF': {
                '4⭐️': ['DIMARCO', 'E.ZEBALLOS']
            },
            'RMF': {
                '5⭐️': ['GIULIANO SIMEONE'],
                '4⭐️': ['DENZEL DUMFRIES', 'ALEXIS SAELEMAEKERS', 'MAGHNES AKLIOUCHE']
            },
            'CMF': {
                '4⭐️': ['S.MILINKOVIC SAVIC', 'JOHN MCGINN', 'LAIMER', 'GAVI', 'SABITZER', 'GUNDOGAN', 'PAPE MATAR SARR', 'CONOR GALLAGHER', 'JOELINTON', 'BRAIS MENDEZ', 'VERATTI', 'TIELEMANS']
            },
            'DMF': {
                '4⭐️': ['ANDRE', 'LUCAS TORREIRA', 'EZEQUIEL FERNANDES', 'LOBOTKA', 'ALAN VARELA', 'CASEMIRO', 'TYLER ADAMS', 'A.STILLER', 'MILTON DELGADO', 'RICCI', 'FRANCO IBARRA', 'MIKEL JAUREGIZAR']
            },
            'LB': {
                '5⭐️': ['CALAFIORI'],
                '4⭐️': ['GUTIERREZ', 'ANTONEE ROBINSON', 'SERGI CARDONA', 'NICO O REILLY', 'JORREL HATO', 'M.LEWIS SKELLY', 'A. TRUFFERT', 'IAN MAATSEN']
            },
            'RB': {
                '4⭐️': ['DI LORENZO', 'SACHA BOEY', 'LLORENTE', 'FRIMPONG', 'REECE JAMES', 'TOMIYASU', 'MALO GUSTO', 'RICO LEWIS']
            },
            'CB': {
                '5⭐️': ['C.ROMERO'],
                '4⭐️': ['DE VRIJ', 'LOIC BADE', 'DAVINSON SANCHEZ', 'ACERBI', 'JOACHIM ANDERSON', 'AGUERD', 'KOSSOUNOU', 'MATTEO GABBIA', 'HIROKI ITO', 'EVAN NDICKA', 'LACROIX']
            },
            'GK': {
                '5⭐️': ['THIBAUT COURTOIS'],
                '4⭐️': ['OLIVER BAUMANN', 'MILE SVILAR', 'HRADECKY', 'BRICE SAMBA', 'KELLEHER', 'TRUBIN', 'BERND LENO', 'CARNESECCHI', 'ALEX REMIRO']
            }
        }
        
        players_added = 0
        for pos, ratings_dict in player_data.items():
            for rating, names in ratings_dict.items():
                base_price = 70.00 if rating == '5⭐️' else 50.00
                for name in names:
                    if not Player.objects.filter(name=name.title(), team__isnull=True).exists():
                        Player.objects.create(
                            name=name.title(),
                            position=pos,
                            rating=rating,
                            market_value=base_price,
                            playing_style="Standard"
                        )
                        players_added += 1
                        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {players_added} auction players!'))
