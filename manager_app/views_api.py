from manager_app.models import Reservation
from rest_framework import generics
from manager_app.serializers import ReservationSerializer


class ReservationViewSet(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
