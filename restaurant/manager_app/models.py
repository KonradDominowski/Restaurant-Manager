from datetime import datetime, timedelta

from django.db import models

hour_list = [(datetime(1000, 1, 1, hour=10) + i * timedelta(minutes=15)).time() for i in range(53)]
HOUR_CHOICES = zip(hour_list, hour_list)


# TODO - Add fields: reservation confirmed and advance payment
# TODO - Handle timeslots for reservations of the same table
# TODO - Handle duplicate reservations of the same table - unique together
class Reservation(models.Model):
    name = models.CharField(max_length=128)
    guest_number = models.PositiveIntegerField()
    date = models.DateField(null=True)
    hour = models.TimeField(null=True, choices=HOUR_CHOICES)
    table = models.ForeignKey('Table', on_delete=models.CASCADE, null=True)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, null=True)
    extra_info = models.ManyToManyField('ExtraInfo', through='ReservationExtraInfo')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name, self.date


class Table(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=128, unique=True)
    prepared = models.BooleanField()
    dishes = models.ManyToManyField('Dish')
    price = models.FloatField()
    active = models.BooleanField()

    def __str__(self):
        return self.name


DISH_CATEGORY = (
    ('Przystawka', 'Przystawka',),
    ('Zupa', 'Zupa',),
    ('Danie główne', 'Danie główne',),
    ('Deser', 'Deser',),
)


class Dish(models.Model):
    name = models.CharField(max_length=128)
    category = models.CharField(max_length=32, choices=DISH_CATEGORY)
    price = models.FloatField()

    def __str__(self):
        return self.name


class ExtraInfo(models.Model):
    vegetarian = models.BooleanField(default=False)
    vegan = models.BooleanField(default=False)
    celiac = models.BooleanField(default=False)
    peanut_allergy = models.BooleanField(default=False)
    dairy = models.BooleanField(default=False)
    child_seat = models.BooleanField(default=False)


class ReservationExtraInfo(models.Model):
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    info = models.ForeignKey('ExtraInfo', on_delete=models.CASCADE)
    amount = models.IntegerField()
