from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form

from .models import Dish, Reservation, Menu, Table, ExtraInfo


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
                                           label='Zupa')
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


class SelectTableForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['table']


class ChangeGuestNumberForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['guest_number']


class SelectMenuForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['menu']


class ExtraInfoForm(ModelForm):
    class Meta:
        model = ExtraInfo
        fields = '__all__'
        widgets = {
            'reservation': forms.HiddenInput(),
        }


class DateRangeForm(Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Początek')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Koniec')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']

        if start_date and end_date:
            if end_date < start_date:
                raise ValidationError('Data końcowa jest większa od początkowej')
