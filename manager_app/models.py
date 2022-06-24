from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import models

hour_list = [(datetime(1000, 1, 1, hour=10) + i * timedelta(minutes=15)).time() for i in range(53)]
HOUR_CHOICES = zip(hour_list, hour_list)
RESERVATION_DURATION = 3


# TODO - Add fields: reservation confirmed and advance payment
class Reservation(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nazwa rezerwacji')
    guest_number = models.PositiveIntegerField(verbose_name='Ilość gości')
    date = models.DateField(null=True, verbose_name='Data')
    hour = models.TimeField(null=True, choices=HOUR_CHOICES, verbose_name='Godzina')
    end_hour = models.TimeField(null=True, choices=HOUR_CHOICES, verbose_name='Godzina zakończenia')
    table = models.ForeignKey('Table', on_delete=models.CASCADE, null=True, verbose_name='Stół')
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, null=True, verbose_name='Menu')
    notes = models.TextField(null=True, verbose_name='Notatki')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Utworzono')
    updated = models.DateTimeField(auto_now=True, verbose_name='Zaktualizowano')

    # FIXME - Jeśli ta metoda jest użyta w save, to nie trzeba ręcznie wywoływać clean za każdym razem przed save, 
    #  ale nie wyświetlają się błędy w formularzu i trzeba je ręcznie dodać
    def table_is_free(self):
        """Return True if table is available for a reservation for given hour,
        reservation duration is set by default to 3 hours."""

        if self.table:
            table_reservations = Reservation.objects.filter(date=self.date, table=self.table).exclude(id=self.id)
            for res in table_reservations:
                if res.hour <= self.hour < res.end_hour:
                    raise ValidationError(f'{self.table} jest już zajęty, jest zarezerwowany na {res.hour}')
                if self.hour < res.hour < self.end_hour:
                    raise ValidationError(f'{self.table} jest już zajęty, jest zarezerwowany na {res.hour}')
        return True
        
    def clean(self):
        self.end_hour = self.hour.replace(hour=(self.hour.hour + RESERVATION_DURATION) % 24)
        self.table_is_free()
        super(Reservation, self).clean()
        
    def save(self, *args, **kwargs):
        # self.end_hour = self.hour.replace(hour=(self.hour.hour + RESERVATION_DURATION) % 24)
        # self.table_is_free()
        super(Reservation, self).save()
        
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
    prepared = models.BooleanField(default=True)
    dishes = models.ManyToManyField('Dish', verbose_name='Dania')
    price = models.FloatField(verbose_name='Cena')
    active = models.BooleanField(default=True)

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
    """This model can expand over time, with more additional reservation info being added."""

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
        text = ''
        for name, value in self.get_fields():
            text += f'{name}: {value}\n'
        return text

    def get_fields(self):
        return [(field.verbose_name, getattr(self, field.name)) for field in ExtraInfo._meta.fields]
