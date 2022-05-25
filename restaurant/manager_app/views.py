from datetime import date, timedelta

from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import CreateReservationForm, SelectTableForm, SelectMenuForm, ExtraInfoForm
from .models import Reservation, Dish, Menu, Table, ExtraInfo


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_dishes_by_type():
    dishes = {
        'przystawka_grupowa': Dish.objects.filter(category='Przystawka grupowa'),
        'przystawka': Dish.objects.filter(category='Przystawka'),
        'zupa': Dish.objects.filter(category='Zupa'),
        'danie_glowne': Dish.objects.filter(category='Danie główne'),
        'deser': Dish.objects.filter(category='Deser'),
    }
    return dishes


class IndexView(View):
    def get(self, request):
        today = date.today()
        reservations = Reservation.objects.filter(date=today).order_by('hour')
        all_guests = sum(i.guest_number for i in reservations)
        ctx = {
            'date': today,
            'reservations': reservations,
            'amount': reservations.count(),
            'all_guests': all_guests
        }
        return render(request, 'index.html', ctx)


class CreateDishView(CreateView):
    model = Dish
    fields = '__all__'
    success_url = '/menu/dish/add/'
    template_name = 'dish-add.html'


class CreateReservationView(View):
    def get(self, request):
        form = CreateReservationForm()
        if request.GET.get('date'):
            raw_date = request.GET.get('date').split(',')
            res_date = date(int(raw_date[0]), int(raw_date[1]), int(raw_date[2]))
            form = CreateReservationForm(initial={'date': res_date})
        return render(request, 'reservations-add.html', {'form': form})

    def post(self, request):
        form = CreateReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('upcoming-reservations'))
        else:
            form = CreateReservationForm(initial=form.cleaned_data)
            return render(request, 'reservations-add.html', {'form': form})


class UpcomingReservationsView(ListView):
    """
    Shows all reservations scheduled in the following 2 weeks.
    """
    model = Reservation
    template_name = 'reservations-upcoming.html'
    context_object_name = 'reservations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        end_date = today + timedelta(days=14)
        queryset = Reservation.objects.filter(date__gte=today, date__lte=end_date).order_by('date', 'hour')
        context['reservations'] = queryset
        context['date_range'] = daterange(today, end_date)
        context['res_date'] = sorted(list(set([res.date for res in queryset])))
        return context


class CreateMenuView(View):
    def get(self, request):
        ctx = get_dishes_by_type()
        return render(request, 'menu-add.html', ctx)

    def post(self, request):
        name = request.POST.get('name')
        price = int(request.POST.get('price'))
        dishes = [name for name, value in request.POST.items() if value == 'on']
        dishes_query_set = [Dish.objects.get(name=name) for name in dishes]
        ctx = get_dishes_by_type()
        ctx['name'] = name
        ctx['price'] = price
        ctx['dishes'] = dishes_query_set
        if name != '' and price > 0:
            try:
                new_menu = Menu(name=name, prepared=True,
                                price=price, active=True)
                new_menu.save()
                for dish in dishes_query_set:
                    new_menu.dishes.add(dish)
                return redirect(reverse_lazy('menu-details', kwargs={'menu_id': new_menu.id}))
            except IntegrityError:
                ctx['message'] = 'Menu o takiej nazwie już istnieje'
                return render(request, 'menu-add.html', ctx)
        else:
            ctx['message'] = 'Cena musi być powyżej 0'
            return render(request, 'menu-add.html', ctx)


class DetailMenuView(ListView):
    model = Menu
    context_object_name = 'menu'
    template_name = 'menu-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Menu.objects.get(id=self.kwargs['menu_id'])
        print(Menu.objects.get(id=self.kwargs['menu_id']))
        return context


class MenuListView(ListView):
    model = Menu
    template_name = 'menu-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menus'] = Menu.objects.filter(active=True).order_by('name')
        return context


class DishListView(ListView):
    model = Dish
    template_name = 'dish-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in get_dishes_by_type().items():
            context[key] = value
        return context


class ReservationDetailView(View):
    def get(self, request, res_id):
        reservation = Reservation.objects.get(id=res_id)
        tables = Table.objects.all()
        table_form = SelectTableForm(initial={'reservation': reservation})
        menu_form = SelectMenuForm(initial={'reservation': reservation})
        extra_info_form = ExtraInfoForm(initial={'reservation': reservation})
        ctx = {
            'res': reservation,
            'tables': tables,
            'table_form': table_form,
            'menu_form': menu_form,
            'extra_info_form': extra_info_form
        }
        try:
            extra_info = ExtraInfo.objects.get(reservation=reservation)
            initial_dict = {key: value for key, value in extra_info.get_fields()}
            ctx['extra_info'] = extra_info
            ctx['extra_info_form'] = ExtraInfoForm(initial=initial_dict)
        except ExtraInfo.DoesNotExist:
            pass
        return render(request, 'reservations-details.html', ctx)


class SaveTableToReservation(View):
    def post(self, request, res_id):
        form = SelectTableForm(request.POST)
        if form.is_valid():
            reservation = form.cleaned_data['reservation']
            reservation.table = form.cleaned_data['table']
            reservation.save()
        return redirect(reverse('reservation-details', kwargs={'res_id': res_id}))


class SaveMenuToReservation(View):
    def post(self, request, res_id):
        form = SelectMenuForm(request.POST)
        if form.is_valid():
            reservation = form.cleaned_data['reservation']
            reservation.menu = form.cleaned_data['menu']
            reservation.save()
        return redirect(reverse('reservation-details', kwargs={'res_id': res_id}))


class RemoveMenuFromReservation(View):
    def post(self, request, res_id):
        reservation = Reservation.objects.get(id=res_id)
        reservation.menu = None
        reservation.save()
        return redirect(reverse('reservation-details', kwargs={'res_id': res_id}))


class SaveInfoToReservation(View):
    def post(self, request, res_id):
        reservation = Reservation.objects.get(id=res_id)

        try:
            extra_info = ExtraInfo.objects.get(reservation=reservation)
        except ExtraInfo.DoesNotExist:
            extra_info = ExtraInfo.objects.create(reservation=reservation)
        form = ExtraInfoForm(request.POST, instance=extra_info)

        if form.is_valid():
            form.save()
        return redirect(reverse('reservation-details', kwargs={'res_id': res_id}))


class ReservationsSearchView(View):
    def get(self, request):
        reservations = Reservation.objects.all()
        ctx = {
            'reservations': reservations
        }
        return render(request, 'reservations-search.html', ctx)

    def post(self, request):
        search = request.POST.get('search')
        try:
            reservations = Reservation.objects.filter(name__icontains=search).order_by('date')
            ctx = {
                'reservations': reservations
            }
        except Reservation.DoesNotExist:
            return HttpResponse('Nie istnieją takie rezerwacje')
        return render(request, 'reservations-search.html', ctx)
