from django.core.management.base import BaseCommand
from ._private import *


class Command(BaseCommand):
    help = 'Populates restaurant with sample dishes, menus and reservations'

    def handle(self, *args, **options):
        add_starters()
        add_dishes()
        create_reservations()
        create_menus()
        add_menus_to_reservations()
        self.stdout.write(self.style.SUCCESS("Successfully populated restaurant "
                                             "with sample dishes, menus and reservations"))
