from datetime import datetime, timedelta

from django.db import models

hour_list = [(datetime(1000, 1, 1, hour=10) + i * timedelta(minutes=15)).time() for i in range(53)]
HOUR_CHOICES = zip(hour_list, hour_list)


# TODO - Add fields: reservation confirmed and advance payment
# TODO - Handle timeslots for reservations of the same table
# TODO - Handle duplicate reservations of the same table - unique together
class Reservation(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nazwa rezerwacji')
    guest_number = models.PositiveIntegerField(verbose_name='Ilość gości')
    date = models.DateField(null=True, verbose_name='Data')
    hour = models.TimeField(null=True, choices=HOUR_CHOICES, verbose_name='Godzina')
    table = models.ForeignKey('Table', on_delete=models.CASCADE, null=True, verbose_name='Stół')
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, null=True, verbose_name='Menu')
    notes = models.TextField(null=True, verbose_name='Notatki')
    # extra_info = models.OneToOneField('ExtraInfo', on_delete=models.CASCADE, null=True,
    #                                   verbose_name='Dodatkowe informacje')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')
    updated = models.DateTimeField(auto_now=True, verbose_name='Zaktualizowano')

    def __str__(self):
        return f'{self.name}, {self.date}'

    def __repr__(self):
        return f'{self.name}, {self.date}'


class Table(models.Model):
    name = models.CharField(max_length=64, verbose_name='Stół')
    capacity = models.IntegerField(verbose_name='Ilość miejsc')

    def __str__(self):
        return f'{self.name}'


class Menu(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='Nazwa Menu')
    prepared = models.BooleanField()
    dishes = models.ManyToManyField('Dish', verbose_name='Dania')
    price = models.FloatField(verbose_name='Cena')
    active = models.BooleanField()

    def __str__(self):
        return f'{self.name}'


DISH_CATEGORY = (
    ('Przystawka', 'Przystawka',),
    ('Przystawka grupowa', 'Przystawka grupowa',),
    ('Zupa', 'Zupa',),
    ('Danie główne', 'Danie główne',),
    ('Deser', 'Deser',),
)


class Dish(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nazwa Dania')
    category = models.CharField(max_length=32, choices=DISH_CATEGORY, verbose_name='Kategoria')
    price = models.FloatField(verbose_name='Cena')

    def __str__(self):
        return f'{self.name}'


class ExtraInfo(models.Model):
    reservation = models.OneToOneField('Reservation', on_delete=models.CASCADE, verbose_name='Rezerwacja',
                                       primary_key=True)
    vegetarian = models.PositiveIntegerField(default=0, verbose_name='Dieta wegetariańska')
    vegan = models.PositiveIntegerField(default=0, verbose_name='Dieta wegańska')
    celiac = models.PositiveIntegerField(default=0, verbose_name='Celiakia')
    peanut_allergy = models.PositiveIntegerField(default=0, verbose_name='Alergia na orzechy')
    dairy = models.PositiveIntegerField(default=0, verbose_name='Dieta beznabiałowa')
    child_seat = models.PositiveIntegerField(default=0, verbose_name='Krzesełko dla dziecka')

    def __str__(self):
        text = ''
        for name, value in self.get_fields():
            text += f'{name}: {value}\n'
        return text

    def __repr__(self):
        return str(self.reservation)

    def get_fields(self):
        return [(field.name, getattr(self, field.name)) for field in ExtraInfo._meta.fields]
