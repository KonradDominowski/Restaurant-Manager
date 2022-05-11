from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Dish, Reservation, Menu, Table


def date_is_in_the_future(date_to_check):
    if (date.today() - date_to_check).days > 0:
        raise ValidationError(f'{date_to_check} jest w przeszłości')


class CreateDishForm(ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'


class CreateReservationForm(ModelForm):
    date = forms.DateField(validators=[date_is_in_the_future], widget=forms.DateInput(attrs={'type': 'date'}))
    table = forms.ModelChoiceField(Table.objects.all(), required=False)
    menu = forms.ModelChoiceField(Menu.objects.all(), required=False)

    class Meta:
        model = Reservation
        fields = ['date', 'name', 'guest_number', 'hour', 'table', 'menu']


class CreateMenuForm(ModelForm):
    dishes = forms.ModelMultipleChoiceField(Dish.objects.all(), widget=forms.CheckboxSelectMultiple)
    prepared = forms.BooleanField(initial=True)

    class Meta:
        model = Menu
        fields = '__all__'
