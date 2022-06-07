import pytest
from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from manager_app.models import *
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

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
