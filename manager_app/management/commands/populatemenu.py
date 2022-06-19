from django.core.management.base import BaseCommand
from ._private import create_menus


class Command(BaseCommand):
    help = 'Populates restaurant with menus.'

    def handle(self, *args, **options):
        create_menus()
        self.stdout.write(self.style.SUCCESS("Successfully populated restaurant with menus"))
