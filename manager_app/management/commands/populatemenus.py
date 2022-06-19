from django.core.management.base import BaseCommand
from ._private import add_menus_to_reservations


class Command(BaseCommand):
    help = 'Populates restaurant with menus.'

    def handle(self, *args, **options):
        add_menus_to_reservations()
        self.stdout.write(self.style.SUCCESS("Successfully populated added menus to some reservations"))
