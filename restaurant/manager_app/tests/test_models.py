from datetime import time, date

import pytest
from django.contrib.auth.models import User

from manager_app.models import *

pytestmark = pytest.mark.django_db


class TestUsers:
    def test_adding_user(self):
        User.objects.create_user('test', 'test@test.com', 'test')
        assert User.objects.count() == 1

    def test_adding_super_user(self):
        User.objects.create_superuser('test', 'test@test.com', 'test')
        assert User.objects.filter(is_superuser=True).count() == 1

    def test_changing_password(self):
        user = User('test', 'test@test.com', 'test')
        user.set_password('test_new_password')
        assert User.check_password(user, 'test_new_password')


class TestMenus:
    @pytest.fixture()
    def menu_1(self):
        print('creating menu')
        return Menu.objects.create(name='Test Menu', price='10', prepared=True, active=True)

    def test_menu_adding(self, menu_1):
        assert Menu.objects.count() == 1

    def test_menu_price_change(self, menu_1):
        menu_1.price = 20
        assert menu_1.price == 20

    def test_menu_name_change(self, menu_1):
        menu_1.name = 'test name for a menu'
        assert menu_1.name == 'test name for a menu'

    def test_menu_archive(self, menu_1):
        menu_1.active = False
        assert not menu_1.active


class TestDishes:
    @pytest.fixture()
    def dish_1(self):
        print('creating dish')
        return Dish.objects.create(name='Test dish', category='Test category', price=10)

    def test_dish_adding(self, dish_1):
        assert Dish.objects.count() == 1

    def test_dish_price_change(self, dish_1):
        dish_1.price = 20
        assert dish_1.price == 20

    def test_dish_category_change(self, dish_1):
        dish_1.category = 'New testing category'
        assert dish_1.category == 'New testing category'


class TestReservations:
    @pytest.fixture()
    def table_1(self):
        return Table.objects.create(name='Test table', capacity=10)

    @pytest.fixture()
    def reservation_1(self, table_1):
        res = Reservation(name='Test',
                          guest_number=10,
                          date=date(2000, 1, 1),
                          hour=time(20, 00, 00),
                          table_id=table_1.id)
        res.clean()  # atrybut end_hour jest ustawiany w metodzie clean, dlatego jest ona tutaj wywołana
        res.save()
        return res

    def test_reservation_adding(self, reservation_1):
        assert Reservation.objects.count() == 1

    def test_reservation_deleting(self, reservation_1):
        reservation_1.delete()
        assert Reservation.objects.count() == 0

    def test_reservation_end_hour(self, reservation_1):
        assert reservation_1.end_hour == time(23, 00, 00)

    def test_reservation_guest_number_change(self, reservation_1):
        reservation_1.guest_number = 20
        assert reservation_1.guest_number == 20

    def test_reservation_date_change(self, reservation_1):
        reservation_1.date = date(2021, 1, 3)
        assert reservation_1.date == date(2021, 1, 3)

    def test_reservation_name_change(self, reservation_1):
        reservation_1.name = 'new test name'
        assert reservation_1.name == 'new test name'

    def test_table_is_free_sooner_hour(self, reservation_1, table_1):
        res2 = Reservation(name='Test2',
                           guest_number=10,
                           date=date(2000, 1, 1),
                           hour=time(19, 00, 00),
                           table_id=table_1.id)
        with pytest.raises(ValidationError):
            res2.clean()

    def test_table_is_free_later_hour(self, reservation_1, table_1):
        res2 = Reservation(name='Test2',
                           guest_number=10,
                           date=date(2000, 1, 1),
                           hour=time(22, 00, 00),
                           table_id=table_1.id)
        with pytest.raises(ValidationError):
            res2.clean()

    def test_table_is_free_same_hour(self, reservation_1, table_1):
        res2 = Reservation(name='Test2',
                           guest_number=10,
                           date=date(2000, 1, 1),
                           hour=time(20, 00, 00),
                           table_id=table_1.id)
        with pytest.raises(ValidationError):
            res2.clean()
