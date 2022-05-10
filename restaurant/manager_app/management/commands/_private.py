from random import randint, randrange
from datetime import datetime, timedelta
from faker import Factory
from manager_app.models import Reservation


def create_name():
    fake = Factory.create("pl_PL")
    last_name = fake.last_name()
    return last_name


def generate_random_date(start_date: datetime, end_date: datetime, amount):
    days_between_dates = (end_date - start_date).days
    dates = []
    for i in range(amount):
        random_date = start_date + timedelta(days=randrange(days_between_dates))
        random_date += randrange(1, 28) * timedelta(minutes=30)
        dates.append(random_date)
    return dates


def create_reservations():
    start = datetime(2020, 1, 1, 10, 0, 0)
    end = datetime(2022, 1, 1, 10, 0, 0)
    for date in generate_random_date(start, end, 100):
        last_name = create_name()
        Reservation.objects.create(name=last_name,
                                   guest_number=randint(10, 50),
                                   date_hour=date)
