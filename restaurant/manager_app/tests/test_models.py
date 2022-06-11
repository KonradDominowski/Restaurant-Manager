from datetime import time, date

import pytest
from django.contrib.auth.models import User

from manager_app.models import *

pytestmark = pytest.mark.django_db


@pytest.fixture()
def reservation_1(table_1):
    res = Reservation(name='Test',
                      guest_number=10,
                      date=date(2000, 1, 1),
                      hour=time(20, 00, 00),
                      table_id=table_1.id)
    res.clean()
    res.save()
    return res


@pytest.fixture()
def table_1():
    return Table.objects.create(name='Test table', capacity=10)


@pytest.fixture()
def table_2():
    return Table.objects.create(name='Second test table', capacity=20)


@pytest.fixture()
def dish_1():
    return Dish.objects.create(name='Test dish', category='Test category', price=10)


@pytest.fixture()
def dish_2():
    return Dish.objects.create(name='Second test dish', category='Test category 2', price=15)


@pytest.fixture()
def menu_1():
    return Menu.objects.create(name='Test Menu', price='10', prepared=True, active=True)


@pytest.fixture()
def menu_2():
    return Menu.objects.create(name='Second test Menu', price='30', prepared=True, active=True)


@pytest.fixture()
def extra_info_1(reservation_1):
    return ExtraInfo.objects.create(vegetarian=1,
                                    vegan=2,
                                    celiac=3,
                                    peanut_allergy=4,
                                    dairy=5,
                                    child_seat=6,
                                    reservation=reservation_1)


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
    def test_dish_adding(self, dish_1):
        assert Dish.objects.count() == 1

    def test_dish_price_change(self, dish_1):
        dish_1.price = 20
        assert dish_1.price == 20

    def test_dish_category_change(self, dish_1):
        dish_1.category = 'New testing category'
        assert dish_1.category == 'New testing category'

    def test_dish_deleting(self, dish_1):
        dish_1.delete()
        assert Dish.objects.count() == 0


class TestReservations:
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


class TestTables:
    def test_table_adding(self, table_1):
        assert Table.objects.count() == 1

    def test_table_name_change(self, table_1):
        table_1.name = 'New table'
        assert table_1.name == 'New table'

    def test_table_capacity_change(self, table_1):
        table_1.capacity = 20
        assert table_1.capacity == 20


class TestExtraInfo:
    def test_extra_info_adding(self, extra_info_1):
        assert ExtraInfo.objects.count() == 1

    def test_extra_info_modifications(self, extra_info_1):
        extra_info_1.dairy = 0
        assert extra_info_1.dairy == 0

        extra_info_1.celiac = 7
        assert extra_info_1.celiac == 7

        extra_info_1.vegan = 1
        assert extra_info_1.vegan == 1

        extra_info_1.child_seat = 8
        assert extra_info_1.child_seat == 8


class TestRelations:
    def test_changing_table(self, reservation_1, table_1, table_2):
        reservation_1.table = table_2
        assert reservation_1.table == table_2

    def test_table_is_free_sooner_hour(self, reservation_1, table_1):
        res2 = Reservation(name='Test2',
                           guest_number=10,
                           date=date(2000, 1, 1),
                           hour=time(19, 00, 00),
                           table_id=table_1.id)
        with pytest.raises(ValidationError):
            res2.clean()
            res2.save()

    def test_table_is_free_later_hour(self, reservation_1, table_1):
        res2 = Reservation(name='Test2',
                           guest_number=10,
                           date=date(2000, 1, 1),
                           hour=time(22, 00, 00),
                           table_id=table_1.id)
        with pytest.raises(ValidationError):
            res2.clean()
            res2.save()

    def test_table_is_free_same_hour(self, reservation_1, table_1):
        res2 = Reservation(name='Test2',
                           guest_number=10,
                           date=date(2000, 1, 1),
                           hour=time(20, 00, 00),
                           table_id=table_1.id)
        with pytest.raises(ValidationError):
            res2.clean()
            res2.save()

    def test_menu_adding_to_reservation(self, reservation_1, menu_1):
        reservation_1.menu = menu_1
        assert reservation_1.menu == menu_1

    def test_menu_changing_reservation(self, reservation_1, menu_1, menu_2):
        reservation_1.menu = menu_1
        reservation_1.menu = menu_2
        assert reservation_1.menu == menu_2

    def test_menu_deleting_from_reservation(self, reservation_1, menu_1):
        reservation_1.menu = menu_1
        assert reservation_1.menu == menu_1

        reservation_1.menu = None
        assert reservation_1.menu is None

    def test_menu_adding_dishes(self, menu_1, dish_1, dish_2):
        menu_1.dishes.add(dish_1)
        assert menu_1.dishes.count() == 1

        menu_1.dishes.add(dish_2)
        assert menu_1.dishes.count() == 2

    def test_menu_removing_dishes(self, menu_1, dish_1, dish_2):
        menu_1.dishes.add(dish_1)
        menu_1.dishes.add(dish_2)
        assert menu_1.dishes.count() == 2

        menu_1.dishes.remove(dish_1)
        assert menu_1.dishes.count() == 1

        menu_1.dishes.remove(dish_2)
        assert menu_1.dishes.count() == 0
