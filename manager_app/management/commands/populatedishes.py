from django.core.management.base import BaseCommand
from ._private import add_dishes


class Command(BaseCommand):
    help = 'Populates restaurant with dishes.'

    def handle(self, *args, **options):
        add_dishes()
        self.stdout.write(self.style.SUCCESS("Successfully populated restaurant with dishes"))
