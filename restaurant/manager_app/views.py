from datetime import date, timedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import CreateReservationForm, CreateMenuForm, SelectTableForm, SelectMenuForm, ExtraInfoForm
from .models import Reservation, Dish, Menu, Table, ExtraInfo


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class IndexView(View):
    def get(self, request):
        today = date.today()
        reservations = Reservation.objects.filter(date=today).order_by('hour')
        all_guests = sum(i.guest_number for i in reservations)
        ctx = {
            'today': today,
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


# TODO redirect to reservation list or details
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


class CreateMenuView(CreateView):
    model = Menu
    form_class = CreateMenuForm
    template_name = 'menu-add.html'

    # queryset = Dish.objects.order_by('-category').order_by('id')

    def form_valid(self, form):
        data = form.cleaned_data
        data['dishes'] = data['group_apps'] | data['starters'] | data['soups'] | data['main_courses'] | data['desserts']
        print(data)
        form.save()
        menu_id = Menu.objects.get(name=data['name']).id
        return redirect(reverse_lazy('menu-details', kwargs={'menu_id': menu_id}))


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
    context_object_name = 'menus'
    template_name = 'menu-list.html'


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
            ctx['extra_info'] = extra_info
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


# TODO maybe extra info needs a different approach?
# TODO ExtraInfo saves but it doesn't add to reservation
class SaveInfoToReservation(View):
    def post(self, request, res_id):
        form = ExtraInfoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('reservation-details', kwargs={'res_id': res_id}))
