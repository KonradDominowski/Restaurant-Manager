from datetime import time, date
from unittest import TestCase

import pytest
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from manager_app.models import *

pytestmark = pytest.mark.django_db


def reservation_1():
    return Reservation.objects.create(
        date=date.today(),
        name='Test 1',
        guest_number=10,
        hour=time(10, 10),
        notes=''
    )


def reservation_2():
    return Reservation.objects.create(
        date=date.today(),
        name='Test 2',
        guest_number=20,
        hour=time(20, 20),
        notes=''
    )


def reservation_3():
    return Reservation.objects.create(
        date=date.today(),
        name='Test 3',
        guest_number=30,
        hour=time(20, 30),
        notes=''
    )


def table_1():
    return Table.objects.create(
        name='Test table',
        capacity=10
    )


def menu_1():
    return Menu.objects.create(
        name='Test menu',
        price=10
    )


def dish_1():
    return Dish.objects.create(
        name='Test dish',
        price=20,
        category='Przystawka'
    )


def dish_2():
    return Dish.objects.create(
        name='Test dish 2',
        price=15,
        category='Przystawka grupowa'
    )


def dish_3():
    return Dish.objects.create(
        name='Test dish',
        price=20,
        category='Zupa'
    )


def dish_4():
    return Dish.objects.create(
        name='Test dish 2',
        price=15,
        category='Danie główne'
    )


def dish_5():
    return Dish.objects.create(
        name='Test dish 2',
        price=15,
        category='Deser'
    )


class TestIndexView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index-view')

    def test_index_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='index.html')

    def test_index_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200


class TestCreateDishView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('dish-add')

    def test_create_dish_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_create_dish_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='dish-add.html')

    def test_create_dish_post_add_to_db(self):
        response = self.client.post(self.url, {
            "name": "Test dish",
            "category": "Przystawka",
            "price": 10
        })

        assert Dish.objects.first().name == 'Test dish'
        assert response.status_code == 302

    def test_create_dish_post_no_data(self):
        response = self.client.post(self.url)

        assert Dish.objects.count() == 0
        assert response.status_code == 200


class TestDishListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.dish_1 = dish_1()
        self.dish_2 = dish_2()
        self.dish_3 = dish_3()
        self.dish_4 = dish_4()
        self.dish_5 = dish_5()
        self.url = reverse('dish-list')

    def test_dish_list_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='dish-list.html')

    def test_dish_list_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_dish_list_all_dishes_are_shown(self):
        response = self.client.get(self.url)
        assert response.context['dish_list'].count() == 5
        assert response.context['przystawka'].count() == 1
        assert response.context['przystawka_grupowa'].count() == 1
        assert response.context['zupa'].count() == 1
        assert response.context['danie_glowne'].count() == 1
        assert response.context['deser'].count() == 1


class TestCreateReservationView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create-reservation')

    def test_create_reservation_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_create_reservation_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='reservations-add.html')

    def test_create_reservation_add_to_db(self):
        response = self.client.post(self.url, {
            'date': date.today(),  # Reservations in the past cannot be added to db, this is futureproof
            'name': 'Test',
            'guest_number': 3,
            'hour': time(11, 45),
            'notes': ''
        })

        assert Reservation.objects.count() == 1
        assert response.status_code == 302


class TestUpcomingReservationsView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('browse-reservations')

    def test_upcoming_reservations_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='reservations-browse.html')

    def test_upcoming_reservations_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_upcoming_reservations_count(self):
        for i in range(1, 20):
            res = Reservation(
                date=date.today() + timedelta(days=i),
                name=f'Test {i}',
                guest_number=i,
                hour=time(i, i),
                notes=''
            )
            res.clean()
            res.save()

        end_date = date.today() + timedelta(days=14)
        reservations = Reservation.objects.filter(date__gte=date.today(),
                                                  date__lte=(end_date + timedelta(days=1))).order_by('date', 'hour')

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.context['reservations'].count() == reservations.count()

        # TODO testy postów dla każdego formularza


class TestReservationDetailView(TestCase):
    def setUp(self):
        self.res = reservation_1()
        self.table = table_1()
        self.client = Client()
        self.url = reverse('reservation-details', args=[self.res.id])

    def test_reservations_details_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_reservations_details_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='reservations-details.html')

    # def test_reservation_details_table_change(self):
    #     response = self.client.post(self.url, {
    #         'table': self.table
    #     })
    #
    #     assert self.res.table == self.table


class TestRemoveMenuFromReservation(TestCase):
    def setUp(self):
        self.res = reservation_1()
        self.menu = menu_1()
        self.res.menu = self.menu
        self.client = Client()
        self.url = reverse('remove-menu', args=[self.res.id])

    def test_remove_menu_post(self):
        response = self.client.post(self.url)
        assert response.status_code == 302

    def test_remove_menu_removing(self):
        assert Reservation.objects.first().menu is None


class TestSaveInfoToReservation(TestCase):
    def test_save_info_post(self):
        self.res = reservation_1()
        self.extra_info = ExtraInfo.objects.create(reservation=self.res)
        self.client = Client()
        self.url = reverse('save-info', kwargs={'res_id': self.res.id})
        data = {
            'reservation': self.res.id,  # Tutaj nie używaj instancji, tylko id, żeby nie siedzieć 2 godziny
            'vegetarian': 1,  # zastanawiając się, dlaczego nie działa
            'vegan': 2,
            'celiac': 3,
            'peanut_allergy': 4,
            'dairy': 5,
            'child_seat': 6}
        response = self.client.post(self.url, data=data)

        assert response.status_code == 302

        self.res.refresh_from_db()
        assert self.res.extrainfo.vegetarian == 1
        assert self.res.extrainfo.vegan == 2
        assert self.res.extrainfo.celiac == 3
        assert self.res.extrainfo.peanut_allergy == 4
        assert self.res.extrainfo.dairy == 5
        assert self.res.extrainfo.child_seat == 6


class TestDeleteReservationView(TestCase):
    def setUp(self):
        self.res = reservation_1()
        self.client = Client()
        self.url = reverse('delete-reservation', kwargs={'res_id': self.res.id})

    def test_remove_reservation_post(self):
        response = self.client.post(self.url)
        assert response.status_code == 302

    def test_remove_reservation_removing(self):
        response = self.client.post(self.url)
        assert Reservation.objects.count() == 0


class TestReservationsSearchView(TestCase):
    def setUp(self):
        self.res_1 = reservation_1()
        self.res_2 = reservation_2()
        self.res_3 = reservation_3()

        self.client = Client()
        self.url = reverse('search-reservations')

    def test_reservations_search_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='reservations-search.html')

    def test_reservations_search_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.context['reservations'].count() == Reservation.objects.count()

    def test_reservations_search_post(self):
        data = {
            'search': 'Test 2'
        }
        response = self.client.post(self.url, data)
        assert response.context['reservations'].count() == 1

        data = {
            'search': 'Test'
        }
        response = self.client.post(self.url, data)
        assert response.context['reservations'].count() == 3


class TestCreateMenuView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create-menu')
        self.user = User.objects.create_user(
            username='test_user',
            password='test_password')
        self.client.force_login(self.user)

    def test_create_menu_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='menu-add.html')

    def test_create_menu_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_create_menu_post(self):
        data = {
            'name': 'Test menu',
            'price': 10
        }
        response = self.client.post(self.url, data)
        assert Menu.objects.count() == 1


class TestEditMenuView(TestCase):
    def setUp(self):
        self.dish_1 = dish_1()
        self.dish_2 = dish_2()
        self.menu = menu_1()
        self.menu.dishes.add(self.dish_1)
        self.client = Client()
        self.url = reverse('edit-menu', kwargs={'menu_id': self.menu.id})

    def test_edit_menu_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='menu-edit.html')

    def test_edit_menu_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_edit_menu_post(self):
        data = {
            'name': 'New Test name',
            'price': 30,
            self.dish_1: 'on',
            self.dish_2: 'on'
        }
        response = self.client.post(self.url, data=data)
        self.menu.refresh_from_db()

        assert response.status_code == 302
        assert self.menu.name == 'New Test name'
        assert self.dish_2 and self.dish_1 in self.menu.dishes.all()
        assert self.menu.dishes.count() == 2

        data = {
            'name': 'New Test name',
            'price': 30,
            self.dish_2: 'on'
        }
        response = self.client.post(self.url, data=data)
        self.menu.refresh_from_db()

        assert response.status_code == 302
        assert self.menu.name == 'New Test name'
        assert self.menu.dishes.count() == 1
        assert self.dish_1 not in self.menu.dishes.all()
        assert self.dish_2 in self.menu.dishes.all()


class TestArchiveMenuView(TestCase):
    def setUp(self):
        self.menu = menu_1()
        self.client = Client()
        self.url = reverse('archive-menu', kwargs={'menu_id': self.menu.id})

    def test_archive_menu_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 302

    def test_archive_menu_archive(self):
        response = self.client.get(self.url)
        assert Menu.objects.filter(active=True).count() == 0


class TestDetailMenuView(TestCase):
    def setUp(self):
        self.dish_1 = dish_1()
        self.menu = menu_1()
        self.menu.dishes.add(dish_1())
        self.client = Client()
        self.url = reverse('menu-details', kwargs={'menu_id': self.menu.id})

    def test_details_menu_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='menu-details.html')

    def test_details_menu_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_details_menu_context(self):
        response = self.client.get(self.url)
        assert self.menu.dishes == response.context['menu'].dishes
        assert self.menu.dishes.count() == response.context['menu'].dishes.count() == 1


class TestMenuListView(TestCase):
    def setUp(self):
        self.menu_1 = menu_1()
        self.client = Client()
        self.url = reverse('menu-list')

    def test_menu_list_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='menu-list.html')

    def test_menu_list_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_menu_list_context(self):
        response = self.client.get(self.url)
        assert response.context['menus'].count() == Menu.objects.filter(active=True).count() == 1


class TestSignUpView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')

    def test_index_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='signup.html')

    def test_index_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_index_post(self):
        data = {
            'username': 'test_user',
            'password': 'test_password',
        }
        response = self.client.post(self.url, data=data)
        assert response.status_code == 302
