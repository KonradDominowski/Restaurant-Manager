from django.core.management.base import BaseCommand
from ._private import add_starters


class Command(BaseCommand):
    help = 'Populates restaurant with starters.'

    def handle(self, *args, **options):
        add_starters()
        self.stdout.write(self.style.SUCCESS("Successfully populated restaurant with starters"))
