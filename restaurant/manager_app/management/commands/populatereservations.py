from django.core.management.base import BaseCommand
from ._private import create_reservations


class Command(BaseCommand):
    help = 'Populates school with grades.'

    def handle(self, *args, **options):
        create_reservations()
        self.stdout.write(self.style.SUCCESS("Succesfully populated restaurant with reservations"))
