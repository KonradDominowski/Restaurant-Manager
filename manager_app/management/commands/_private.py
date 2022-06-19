from random import randint, randrange, choice
from datetime import datetime, timedelta, date
from faker import Factory
from manager_app.models import *
from manager_app.views import get_dishes_by_type


def add_starters():
    starters = (
        ('Mięsa pieczone (450g): schab, karkówka marynowana w ziołach, boczek, cygański', 79),
        ('Pasztet domowy z żurawiną', 39),
        ('Mozzarella z tatarem z pomidorów i świeżą bazylią', 59),
        ('Carpaccio z buraka z serem gorgonzola i pestkami prażonej dyni', 49),
        ('Tortilla z warzywami', 1),
        ('Sałatka cezar z kurczakiem', 1),
        ('Domowe marynaty', 1),
        ('Pieczywo, masło', 1),
        ('Tatar wołowy podawany z siekana cebulą, korniszonem i marynowanymi grzybkami', 95),
        ('Parfait z wątróbki drobiowej podane na grzance ziołowej z rukolą i odrobiną musu figowego, 8szt', 49),
        ('Carpaccio z polędwicy wołowej na rukoli z kaparami i parmezanem', 99),
        ('Smalec z ogórkiem małosolnym (200g)', 19),
        ('Tatar z marynowanego łososia z siekaną czerwoną cebulką, kaparami i czarnymi oliwkami', 95),
        ('Śledzik podawany z cebulką w oleju lub z jabłuszkiem w śmietanie', 49),
        ('Krewetka w tempurze z sosem winno maślanym 8 szt', 49),
        ('Krewetka w sosie orientalnym 8 szt', 49),
        ('Deska 4 rodzajów serów podawana z bakaliami i suszonymi owocami (450g)', 99),
        ('Mini gofry szpinakowe z ziołową ricottą, rukolą i wędzonym łososiem 8 szt', 59),
        ('Marynowane papryczki chilli faszerowane ziołowym serkiem, podawane na rukoli z '
         'grzankami i balsamicznym winegretem 8 szt', 49),
        ('Jajka w majonezie 12 połówek', 25),
        ('Sałata z grillowanym kurczakiem, warzywami julienne i sosem sojowo – imbirowym', 89),
        ('Sałata z liści szpinaku z sosem gorgonzola z orzechami włoskim,i, boczkiem i pomidorkami cherry', 89),
        ('PATERA CIAST (sernik, szarlotka, brownie)', 99),
        ('PATERA OWOCÓW (owoce sezonowe', 99))
    for name, price in starters:
        Dish.objects.create(name=name, category='Przystawka grupowa', price=price)


def add_dishes():
    dishes = (('Śledź w oleju z cebulką', 'Przystawka', 16),
              ('Śledź w śmietanie z jabłkiem', 'Przystawka', 16),
              ('Śledź smażony w zalewie octowej', 'Przystawka', 16),
              ('Tatar z wołowiny z siekaną cebulą, korniszonem i marynowanymi podgrzybkami', 'Przystawka', 32),
              (
                  'Tatar z marynowanego łososia z siekaną czerwoną cebulą, kaparami i czarnymi oliwkami', 'Przystawka',
                  36),
              ('Carpaccio z polędwicy wołowej z oliwą truflową, kaparami parmezanem i rukolą', 'Przystawka', 36),
              ('Deska serów z suszonymi owocami', 'Przystawka', 49),
              ('Rosół z domowym makaronem', 'Zupa', 15),
              ('Tradycyjne flaki wołowe', 'Zupa', 17),
              ('Specjał Galeonu - Zupa Rybna', 'Zupa', 19),
              ('Żur staropolski z białą kiełbasą i jajkiem', 'Zupa', 19),
              ('DESKA GRILLOWANYCH SPECJAŁÓW', 'Danie główne', 89),
              ('Stos Żeberek z sosem BBQ z pikantnym brykietem serowym z frytkami i świeżymi z sałatami z vinaigrettem',
               'Danie główne', 55),
              ('Kaczka pieczona z sosem jabłkowo-żurawinowym z kopytkami i zasmażanymi buraczkami', 'Danie główne', 59),
              ('Golonka gotowana podawana z kapustą zasmażaną, chrzanem i musztardą', 'Danie główne', 49),
              ('Ozorki wołowe w delikatnym sosie chrzanowym z paloną kaszą i chipsami bekonowymi', 'Danie główne', 39),
              ('Tradycyjny kotlet schabowy z purée ziemniaczanym i kapustą zasmażaną', 'Danie główne', 36),
              ('Stripsy z kurczaka z frytkami i z mizerią', 'Danie główne', 29),
              ('Tagliatelle rosso z kurczakiem, szpinakiem, suszonymi pomidorami i parmezanem', 'Danie główne', 36),
              ('Tagliatelle nero z krewetkami (5 szt.), rukolą i pomidorkami cherry', 'Danie główne', 39),
              ('Pieczony filet z łososia na blanszowanym szpinaku z kaszą bulgur i z salsą mango chili', 'Danie główne',
               59),
              (
                  'Dorada pieczona w całości na sałatkach z pomidorem w kraście ziołowym oraz grillowanym ziemniakiem z masłem czosnkowym',
                  'Danie główne', 59),
              (
                  'Sałata z grillowanym kurczakiem, warzywami julienne, kiełkami i sosem sojowo-imbirowym, oprószona sezamem',
                  'Danie główne', 32),
              ('Świeży szpinak z panierowanymi kalmarami (8 szt.) i salsą pomidorową', 'Danie główne', 32),
              ('Sałata z marynowanym łososiem, owocami, pomidorkami cherry i dressingiem mango-chilli', 'Danie główne',
               36),
              ('Krewetki (5 szt.) z warzywami w tempurze, na zielonych sałatach z orientalnym sosem pomarańczowym',
               'Danie główne', 36),
              ('Domowa beza z kremem mascarpone i owocami sezonowymi', 'Deser', 19),
              ('Karmelizowane płatki migdałów z musem mascarpone i świeżymi truskawkami', 'Deser', 19),
              ('Gorący suflet czekoladowy na musie malinowym z lodami waniliowymi', 'Deser', 19),
              ('SpecialMalinowa rozkosz – Lody waniliowe z gorącym musem malinowym', 'Deser', 19),
              ('Szarlotka z lodami waniliowymi', 'Deser', 19),)
    for name, category, price in dishes:
        Dish.objects.create(name=name, category=category, price=price)


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
    for data in generate_random_dates(start, end, 500):
        start_hour = generate_random_hour()
        Reservation.objects.create(name=create_name(),
                                   guest_number=randint(10, 50),
                                   date=data,
                                   hour=start_hour,
                                   end_hour=start_hour.replace(hour=start_hour.hour + RESERVATION_DURATION))


def create_menus():
    all_dishes = get_dishes_by_type()
    prices = [70, 80, 90, 150]
    for i in range(1, 6):
        dishes = []
        for key in all_dishes:
            for _ in range(3):
                dishes.append(choice(all_dishes[key]))
        print(dishes)
        menu = Menu.objects.create(name=f'Przykładowe menu {i}', price=choice(prices))
        menu.dishes.add(*dishes)


def add_menus_to_reservations():
    reservations = Reservation.objects.all()
    menus = Menu.objects.all()
    for index, reservation in enumerate(reservations):
        if index % 2 == 0:
            reservation.menu = choice(menus)
            reservation.save()
