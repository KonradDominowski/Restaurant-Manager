from manager_app.models import Reservation, Menu
from rest_framework import serializers


class ReservationSerializer(serializers.ModelSerializer):
    menu = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='menu-details'
    )

    table = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='table-details'
    )

    class Meta:
        model = Reservation
        fields = [
            'name',
            'guest_number',
            'date',
            'hour',
            'end_hour',
            'table',
            'menu',
            'notes',
            'created',
            'updated',]


# class MenuSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Menu
#         fields = [
#             'name',
#             'prepared',
#             'dishes',
#             'price',
#             'active',
#         ]
# # TODO - serializery wszystkie
