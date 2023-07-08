from django.contrib import admin
from .models import Restaurant, Menu, Reservation, Dish, ExtraInfo

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    pass

@admin.register(Menu)
class RestaurantAdmin(admin.ModelAdmin):
    pass

@admin.register(Reservation)
class RestaurantAdmin(admin.ModelAdmin):
    pass

@admin.register(Dish)
class RestaurantAdmin(admin.ModelAdmin):
    pass

@admin.register(ExtraInfo)
class RestaurantAdmin(admin.ModelAdmin):
    pass

# Register your models here.
