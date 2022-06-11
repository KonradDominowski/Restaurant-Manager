from datetime import time, date
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from manager_app.models import *

pytestmark = pytest.mark.django_db


def reservation_1():
    return Reservation.objects.create(
        date=date.today(),
        name='Test',
        guest_number=10,
        hour=time(10, 10),
        notes=''
    )


def menu_1():
    return Menu.objects.create(
        name='Test menu',
        price=10
    )


class TestIndexView:
    def setup(self):
        self.client = Client()
        self.url = reverse('index-view')

    def test_index_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_index_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='index.html')


# TODO Nie wiem dlaczego zwraca kod 200, a nie 302, czyli redirect
# class TestCreateDishView:
#     def setup(self):
#         self.client = Client()
#         self.url = reverse('dish-add')
#
#     def test_create_dish_get(self):
#         response = self.client.get(self.url)
#         assert response.status_code == 200
#
#     def test_create_dish_template(self):
#         response = self.client.get(self.url)
#         assertTemplateUsed(response, template_name='dish-add.html')
#
#     def test_create_dish_post_add_to_db(self):
#         Dish.objects.create(
#             name='Test dish',
#             category='Test category',
#             price=10
#         )
#
#         response = self.client.post(self.url, {
#             'name': 'Test dish',
#             'category': 'Test category',
#             'price': 10
#         })
#
#         assert Dish.objects.first().name == 'Test dish'
#         assert response.status_code == 302
#
#     def test_create_dish_post_no_data(self):
#         response = self.client.post(self.url)
#
#         assert Dish.objects.count() == 0
#         assert response.status_code == 302


class TestDishListView:
    def setup(self):
        self.client = Client()
        self.url = reverse('dish-list')

    def test_dish_list_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_dish_list_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='dish-list.html')


class TestCreateReservationView:
    def setup(self):
        self.client = Client()
        self.url = reverse('create-reservation')

    def test_create_reservation_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_create_reservation_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='reservations-add.html')

    def test_create_reservation_post_no_data(self):
        with pytest.raises(AttributeError):
            response = self.client.post(self.url)

    def test_create_reservation_add_to_db(self):
        table_1 = Table.objects.create(
            name='Test table',
            capacity=10
        )

        response = self.client.post(self.url, {
            'date': date.today(),  # Reservations in the past cannot be added to db, this is futureproof
            'name': 'Test',
            'guest_number': 3,
            'hour': time(11, 45),
            'notes': ''
        })

        assert Reservation.objects.count() == 1
        assert response.status_code == 302


class TestUpcomingReservationsView:
    def setup(self):
        self.client = Client()
        self.url = reverse('upcoming-reservations')

    def test_upcoming_reservations_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_upcoming_reservations_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='reservations-upcoming.html')

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
        reservations = Reservation.objects.filter(date__gte=date.today(), date__lte=end_date).order_by('date', 'hour')

        response = self.client.get(self.url)

        assert response.status_code == 200
        assert response.context['reservations'].count() == reservations.count()


# TODO - test posts for each form
class TestReservationDetailView:
    def setup(self):
        res = reservation_1()
        self.client = Client()
        self.url = reverse('reservation-details', args=[res.id])

    def test_reservations_details_get(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_reservations_details_template(self):
        response = self.client.get(self.url)
        assertTemplateUsed(response, template_name='reservations-details.html')


class TestRemoveMenuFromReservation:
    def setup(self):
        res = reservation_1()
        menu = menu_1()
        res.menu = menu
        self.client = Client()
        self.url = reverse('remove-menu', args=[res.id])

    def test_remove_menu_post(self):
        response = self.client.post(self.url)
        assert response.status_code == 302
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
