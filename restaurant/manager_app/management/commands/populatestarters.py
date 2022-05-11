from django.core.management.base import BaseCommand
from ._private import add_starters


class Command(BaseCommand):
    help = 'Populates school with grades.'

    def handle(self, *args, **options):
        add_starters()
        self.stdout.write(self.style.SUCCESS("Succesfully populated restaurant with starters"))
