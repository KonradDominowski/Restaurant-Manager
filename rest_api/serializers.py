from rest_framework import serializers
from manager_app.models import Reservation, Restaurant, ExtraInfo, Menu, Table
from django.contrib.auth.models import User

class ExtraInfoSerializer(serializers.ModelSerializer):
    # reservation = serializers.ReadOnlyField(source='reservation.id')
    class Meta:
        model = ExtraInfo
        # fields = '__all__'
        exclude = ('reservation',)

class UserSerializer(serializers.ModelSerializer):
    restaurants = serializers.PrimaryKeyRelatedField(many=True, queryset=Restaurant.objects.all())

    class Meta:
        model = User
        fields = '__all__'
class ReservationSerializer(serializers.ModelSerializer):
    restaurant = serializers.ReadOnlyField(source='restaurant.name')
    extrainfo = ExtraInfoSerializer()

    class Meta:
        model = Reservation
        fields = '__all__'
        # exclude = ('restaurant', )

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'
