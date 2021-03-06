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

from django.contrib import admin
from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from manager_app.views import IndexView, CreateDishView, CreateReservationView, BrowseReservationsView, \
    CreateMenuView, DetailMenuView, MenuListView, ReservationDetailView, SaveInfoToReservation, \
    ReservationsSearchView, DishListView, RemoveMenuFromReservation, DeleteReservation, SignUpView, EditMenuView, \
    ArchiveMenuView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index-view'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('menu/add/', CreateMenuView.as_view(), name='create-menu'),
    path('menu/<int:menu_id>/edit', EditMenuView.as_view(), name='edit-menu'),
    path('menu/<int:menu_id>/archive', ArchiveMenuView.as_view(), name='archive-menu'),
    path('menu/list/', MenuListView.as_view(), name='menu-list'),
    path('menu/<int:menu_id>', DetailMenuView.as_view(), name='menu-details'),
    path('menu/dish/list/', DishListView.as_view(), name='dish-list'),
    path('menu/dish/add/', CreateDishView.as_view(), name='dish-add'),
    path('reservations/add/', CreateReservationView.as_view(), name='create-reservation'),
    path('reservations/browse/', BrowseReservationsView.as_view(), name='browse-reservations'),
    path('reservations/search/', ReservationsSearchView.as_view(), name='search-reservations'),
    path('reservations/details/<int:res_id>', ReservationDetailView.as_view(), name='reservation-details'),
    path('reservations/details/<int:res_id>/removemenu', RemoveMenuFromReservation.as_view(), name='remove-menu'),
    path('reservations/details/<int:res_id>/saveinfo', SaveInfoToReservation.as_view(), name='save-info'),
    path('reservations/details/<int:res_id>/delete', DeleteReservation.as_view(), name='delete-reservation'),
]
