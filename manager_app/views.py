from datetime import date, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from .forms import CreateReservationForm, SelectTableForm, SelectMenuForm, ExtraInfoForm, ChangeGuestNumberForm
from .models import Reservation, Dish, Menu, Table, ExtraInfo


# TODO Wybór dat nadchodzących rezerwacji
# TODO Uwzględnić przeszłe daty w liście rezerwacji


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def get_dishes_by_type():
    dishes = {
        'przystawka_grupowa': Dish.objects.filter(category='Przystawka grupowa').order_by('name'),
        'przystawka': Dish.objects.filter(category='Przystawka').order_by('name'),
        'zupa': Dish.objects.filter(category='Zupa').order_by('name'),
        'danie_glowne': Dish.objects.filter(category='Danie główne').order_by('name'),
        'deser': Dish.objects.filter(category='Deser').order_by('name'),
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
    success_url = '/menu/dish/list/'
    template_name = 'dish-add.html'


class DishListView(ListView):
    """This view displays all dishes in the database, sorted by their category."""

    model = Dish
    template_name = 'dish-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for key, value in get_dishes_by_type().items():
            context[key] = value
        return context


class CreateReservationView(View):
    """This view is for adding a reservation. """

    def get(self, request):
        form = CreateReservationForm()
        if request.GET.get('date'):
            raw_date = request.GET.get('date').split(',')
            res_date = date(int(raw_date[0]), int(raw_date[1]), int(raw_date[2]))
            form = CreateReservationForm(initial={'date': res_date})
        ctx = {
            'form': form
        }
        try:
            ctx['message'] = self.request.session['message']
            del self.request.session['message']
        except KeyError:
            pass
        return render(request, 'reservations-add.html', ctx)

    def post(self, request):
        form = CreateReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('upcoming-reservations'))
        return render(request, 'reservations-add.html', {'form': form})


# TODO - Add a functionality to change default 2 week time period to whatever user needs
class UpcomingReservationsView(ListView):
    """Shows all reservations scheduled in the following 2 weeks."""

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
        try:
            context['message'] = self.request.session['message']
            del self.request.session['message']
        except KeyError:
            pass
        return context


# TODO - date, hour, name change
class ReservationDetailView(View):
    """
    This view display all details about a reservation. There is a form for each detail,
    so it is possible to change each of them separately.
    """

    def build_context(self, request, res_id):
        reservation = Reservation.objects.get(id=res_id)

        if request.method == 'GET':
            table_form = SelectTableForm(instance=reservation)
            guest_number_form = ChangeGuestNumberForm(instance=reservation)
            menu_form = SelectMenuForm(instance=reservation)
        else:
            table_form = SelectTableForm(request.POST, instance=reservation)
            guest_number_form = ChangeGuestNumberForm(request.POST, instance=reservation)
            menu_form = SelectMenuForm(request.POST, instance=reservation)

        ctx = {
            'res': reservation,
            'table_form': table_form,
            'menu_form': menu_form,
            'guest_number_form': guest_number_form
        }

        try:
            extra_info = ExtraInfo.objects.get(reservation=reservation)
            ctx['extra_info'] = extra_info
            ctx['extra_info_form'] = ExtraInfoForm(instance=extra_info)
        except ExtraInfo.DoesNotExist:
            ctx['extra_info_form'] = ExtraInfoForm(initial={'reservation': reservation})

        return ctx

    def get(self, request, res_id):
        ctx = self.build_context(request, res_id)
        return render(request, 'reservations-details.html', ctx)

    def post(self, request, res_id):
        reservation = Reservation.objects.get(id=res_id)
        table_form = SelectTableForm(request.POST, instance=reservation)
        guest_number_form = ChangeGuestNumberForm(request.POST, instance=reservation)
        menu_form = SelectMenuForm(request.POST, instance=reservation)

        if table_form.is_valid():
            table_form.save()
        if guest_number_form.is_valid():
            guest_number_form.save()
        if menu_form.is_valid():
            menu_form.save()

        ctx = self.build_context(request, res_id)

        return render(request, 'reservations-details.html', ctx)


class RemoveMenuFromReservation(View):
    """View removing assigned menu from a reservation, and then redirecting back to its details."""

    def post(self, request, res_id):
        reservation = Reservation.objects.get(id=res_id)
        reservation.menu = None
        reservation.save()
        return redirect(reverse('reservation-details', kwargs={'res_id': res_id}))


class SaveInfoToReservation(View):
    """View changing extra info of a reservation, and then redirecting back to its details."""

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


class DeleteReservation(View):
    """View deleting a reservation from the database, it adds a session variable notifying the user abot the removal."""

    def post(self, request, res_id):
        reservation = Reservation.objects.get(id=res_id)
        request.session['message'] = f'Usunięto rezerwację <strong>{reservation}</strong>'
        reservation.delete()
        return redirect(reverse('upcoming-reservations'))


class ReservationsSearchView(View):
    """View that shows reservations containing entered phrase."""

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


class CreateMenuView(LoginRequiredMixin, View):
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


class EditMenuView(View):
    def get(self, request, menu_id):
        ctx = get_dishes_by_type()
        menu = Menu.objects.get(id=menu_id)
        ctx['menu'] = menu
        return render(request, 'menu-edit.html', ctx)

    def post(self, request, menu_id):
        menu_to_update = Menu.objects.get(id=menu_id)
        name = request.POST.get('name')
        price = int(float(request.POST.get('price')))
        dishes = [name for name, value in request.POST.items() if value == 'on']
        new_dishes_query_set = [Dish.objects.get(name=name) for name in dishes]
        if name != '' and price > 0:
            menu_to_update.name = name
            menu_to_update.price = price
            # menu_to_update.dishes.clear()  # Pierwsze podejście to usunięcie wszystkich dań,
            # for dish in new_dishes_query_set:  # a potem dodanie wszystkich z formularza
            #     menu_to_update.dishes.add(dish)

            for dish in menu_to_update.dishes.all():  # Drugie podejście to usunięcie tylko dań,
                if dish not in new_dishes_query_set:  # których nie ma w formularzu, a potem dodanie brakujących
                    menu_to_update.dishes.remove(dish)

            for dish in new_dishes_query_set:
                if dish not in menu_to_update.dishes.all():
                    menu_to_update.dishes.add(dish)

            menu_to_update.save()
            return redirect(reverse_lazy('menu-details', kwargs={'menu_id': menu_to_update.id}))


class ArchiveMenuView(View):
    def get(self, request, menu_id):
        menu = Menu.objects.get(id=menu_id)
        menu.active = False
        request.session['message'] = f'Menu <strong>{menu}</strong> zostało zarchiwizowane'
        menu.save()
        return redirect(reverse('menu-list'))


class DetailMenuView(ListView):
    model = Menu
    context_object_name = 'menu'
    template_name = 'menu-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = Menu.objects.get(id=self.kwargs['menu_id'])
        return context


class MenuListView(ListView):
    model = Menu
    template_name = 'menu-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menus'] = Menu.objects.filter(active=True).order_by('name')
        try:
            context['message'] = self.request.session['message']
            del self.request.session['message']
        except KeyError:
            pass
        return context


class SignUpView(View):
    def get(self, request):
        form = UserCreationForm()
        ctx = {
            'form': form
        }
        return render(request, 'signup.html', ctx)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('index-view'))
        return redirect('signup')
