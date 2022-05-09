from django.db import models


class Reservation(models.Model):
    name = models.CharField(max_length=128)
    guest_number = models.PositiveIntegerField()
    date_hour = models.DateTimeField(null=True)
    table = models.ForeignKey('Table', on_delete=models.CASCADE, null=True)
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE, null=True)
    extra_info = models.ManyToManyField('ExtraInfo', through='ReservationExtraInfo')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Table(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()


class Menu(models.Model):
    name = models.CharField(max_length=128)
    prepared = models.BooleanField()
    dishes = models.ManyToManyField('Dish')
    price = models.FloatField()
    active = models.BooleanField()


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


class ExtraInfo(models.Model):
    vegetarian = models.BooleanField()
    vegan = models.BooleanField()
    celiac = models.BooleanField()
    peanut_allergy = models.BooleanField()
    dairy = models.BooleanField()
    child_seat = models.BooleanField()


class ReservationExtraInfo(models.Model):
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE)
    info = models.ForeignKey('ExtraInfo', on_delete=models.CASCADE)
    amount = models.IntegerField()
