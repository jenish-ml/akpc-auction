from django.core.management.base import BaseCommand
from auction.models import Player
import os

class Command(BaseCommand):
    help = "Attach images to players automatically"

    def handle(self, *args, **kwargs):
        base_path = "media/players/"

        count = 0
        for player in Player.objects.all():
            filename = player.name.lower().replace(" ", "_") + ".jpg"
            filepath = os.path.join(base_path, filename)

            if os.path.exists(filepath):
                player.image = f"players/{filename}"
                player.save()
                count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Linked images for {count} players")
        )
