import datetime

from django.forms import ModelForm, Form
from .models import Dish, Reservation, Table
from django import forms
from django.core.exceptions import ValidationError
from datetime import date


def date_is_in_the_future(date_to_check):
    if (date.today() - date_to_check).days > 0:
        raise ValidationError(f'{date_to_check} jest w przeszłości')


class CreateDishForm(ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'


# class CreateReservationForm(Form):
#     date = forms.DateField(validators=[date_is_in_the_future], widget=forms.DateInput(attrs={'type': 'date'}))
#     name = forms.CharField(max_length=128)
#     guest_number = forms.IntegerField()
#     hour = forms.TimeField()
#     table = forms.ModelChoiceField(Table.objects.all())
#     # menu = forms.ModelChoiceField


class CreateReservationForm(ModelForm):
    date = forms.DateField(validators=[date_is_in_the_future], widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Reservation
        fields = ['date', 'name', 'guest_number', 'hour', 'table', 'menu']
        # exclude = ['extra_info']


