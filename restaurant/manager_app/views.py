from datetime import date, time, timedelta

from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView

from .models import Reservation, Dish
from .forms import CreateReservationForm


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
    success_url = '/'
    template_name = 'dish-add.html'


class CreateReservationView(CreateView):
    model = Reservation
    form_class = CreateReservationForm
    success_url = '/'
    template_name = 'reservations-add.html'


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
        next_week = today + timedelta(days=14)
        queryset = Reservation.objects.filter(date__gte=today, date__lte=next_week).order_by('date', 'hour')
        context['reservations'] = queryset
        context['res_date'] = sorted(list(set([res.date for res in queryset])))
        return context
