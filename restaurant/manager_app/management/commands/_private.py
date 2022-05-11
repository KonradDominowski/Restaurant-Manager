from random import randint, randrange
from datetime import datetime, timedelta, date
from faker import Factory
from manager_app.models import Reservation


def create_name():
    fake = Factory.create("pl_PL")
    last_name = fake.last_name()
    return last_name


def generate_random_dates(start_date: date, end_date: date, amount):
    days_between_dates = (end_date - start_date).days
    dates = []
    for _ in range(amount):
        random_date = start_date + timedelta(days=randrange(days_between_dates))
        dates.append(random_date)
    return dates


def generate_random_hour():
    return (datetime(1000, 1, 1, hour=10) + randrange(1, 20) * timedelta(minutes=30)).time()


def create_reservations():
    start = datetime(2022, 1, 1, 10, 0, 0)
    end = datetime(2023, 1, 1, 10, 0, 0)
    for data in generate_random_dates(start, end, 200):
        Reservation.objects.create(name=create_name(),
                                   guest_number=randint(10, 50),
                                   date=data,
                                   hour=generate_random_hour())
