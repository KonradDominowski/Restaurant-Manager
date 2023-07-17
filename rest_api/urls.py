"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from datetime import datetime
from django.urls import path, register_converter
from .views import ReservationListView, UserListView, TodayReservationsList, ReservationDetailsView, ExtraInfoList, \
    DateReservationsList, MenuView, TableView

class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

register_converter(DateConverter, 'date')

urlpatterns = [
    path('reservations/', ReservationListView.as_view(), name='reservations-list'),
    path('reservations/today/', TodayReservationsList.as_view(), name='todays-reservations'),
    path('reservations/<int:res_id>/', ReservationDetailsView.as_view(), name='reservation-detail'),
    path('reservations/<date:start_date>/', DateReservationsList.as_view(), name='dates-reservations-list'),
    path('reservations/<date:start_date>/<date:end_date>/', DateReservationsList.as_view(), name='dates-reservations-list'),
    path('menu/', MenuView.as_view(), name='menu-list'),
    path('menu/<int:menu_id>/', MenuView.as_view(), name='menu-details'),
    path('table/', TableView.as_view(), name='table-list'),
    path('table/<int:table_id>/', TableView.as_view(), name='table-details'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('extra/', ExtraInfoList.as_view(), name='extra-info-list')
]
