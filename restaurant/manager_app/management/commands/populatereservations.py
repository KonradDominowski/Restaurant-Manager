from django.core.management.base import BaseCommand
from ._private import create_reservations


class Command(BaseCommand):
    help = 'Populates restaurant with reservations.'

    def handle(self, *args, **options):
        create_reservations()
        self.stdout.write(self.style.SUCCESS("Successfully populated restaurant with reservations"))
