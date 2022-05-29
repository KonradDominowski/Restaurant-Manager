from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form

from .models import Dish, Reservation, Menu, Table, ExtraInfo

# TODO w środku rozkminiania walidacji pól
def date_is_in_the_future(date_to_check):
    if (date.today() - date_to_check).days > 0:
        raise ValidationError('Nie można dodać rezerwacji w przeszłości.')


def is_positive(number):
    if number <= 0:
        raise ValidationError('Wprowadź liczbę gości powyżej 0.')


class CreateDishForm(ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'


class CreateReservationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'].required = False

    date = forms.DateField(validators=[date_is_in_the_future],
                           widget=forms.DateInput(attrs={'type': 'date'}),
                           label='Data')
    table = forms.ModelChoiceField(Table.objects.all(), required=False, label='Stół')
    menu = forms.ModelChoiceField(Menu.objects.all(), required=False)
    notes = forms.TextInput(attrs={'required': 'false'})

    class Meta:
        model = Reservation
        fields = ['date', 'name', 'guest_number', 'hour', 'table', 'menu', 'notes']


# TODO maybe divide it in a template
class CreateMenuForm(ModelForm):
    group_apps = forms.ModelMultipleChoiceField(Dish.objects.filter(category='Przystawka grupowa').order_by('id'),
                                                widget=forms.CheckboxSelectMultiple,
                                                required=False,
                                                label='Przystawka grupowa')
    starters = forms.ModelMultipleChoiceField(Dish.objects.filter(category='Przystawka').order_by('id'),
                                              widget=forms.CheckboxSelectMultiple,
                                              required=False,
                                              label='Przystawka')
    soups = forms.ModelMultipleChoiceField(Dish.objects.filter(category='Zupa').order_by('id'),
                                           widget=forms.CheckboxSelectMultiple,
                                           required=False,
                                           label='Zupa', )
    main_courses = forms.ModelMultipleChoiceField(Dish.objects.filter(category='Danie główne').order_by('id'),
                                                  widget=forms.CheckboxSelectMultiple,
                                                  required=False,
                                                  label='Danie główne')
    desserts = forms.ModelMultipleChoiceField(Dish.objects.filter(category='Deser').order_by('id'),
                                              widget=forms.CheckboxSelectMultiple,
                                              required=False,
                                              label='Deser')
    prepared = forms.BooleanField(widget=forms.HiddenInput(), initial=True)
    active = forms.BooleanField(widget=forms.HiddenInput(), initial=True)

    class Meta:
        model = Menu
        fields = '__all__'
        widgets = {
            'dishes': forms.HiddenInput(),
        }


class SelectTableForm(Form):
    reservation = forms.ModelChoiceField(Reservation.objects.all(), widget=forms.HiddenInput)
    table = forms.ModelChoiceField(Table.objects.all())


class ChangeGuestNumberForm(Form):
    reservation = forms.ModelChoiceField(Reservation.objects.all(), widget=forms.HiddenInput)
    guests = forms.IntegerField(validators=[is_positive])


class SelectMenuForm(Form):
    reservation = forms.ModelChoiceField(Reservation.objects.all(), widget=forms.HiddenInput)
    menu = forms.ModelChoiceField(Menu.objects.all())


class ExtraInfoForm(ModelForm):
    class Meta:
        model = ExtraInfo
        fields = '__all__'
        widgets = {
            'reservation': forms.HiddenInput(),
        }
