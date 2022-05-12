from datetime import date, timedelta

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import CreateReservationForm, CreateMenuForm
from .models import Reservation, Dish, Menu


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


# class CreateReservationView(CreateView):
#
#     def get_date_param(self):
#         return self.request.GET.get['date']
#
#     date = get_date_param
#     model = Reservation
#     form_class = CreateReservationForm(initial={'guest_number': date})
#     success_url = '/'
#     template_name = 'reservations-add.html'


# TODO redirect to reservation list or details
class CreateReservationView(View):
    def get(self, request):
        raw_date = request.GET.get('date').split(',')
        res_date = date(int(raw_date[0]), int(raw_date[1]), int(raw_date[2]))
        form = CreateReservationForm(initial={'date': res_date})
        return render(request, 'reservations-add.html', {'form': form})

    def post(self, request):
        form = CreateReservationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse('upcoming-reservations'))


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

    def form_valid(self, form):
        form.save()
        menu_id = Menu.objects.get(name=form.cleaned_data['name']).id
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

    # def get_queryset(self):
    #     return Menu.objects.get(id=self.kwargs['menu_id'])
