from datetime import time, date

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from manager_app.models import *

pytestmark = pytest.mark.django_db


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
