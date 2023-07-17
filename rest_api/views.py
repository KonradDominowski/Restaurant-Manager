from datetime import date

from django.contrib.auth.models import User, AnonymousUser
from .serializers import ReservationSerializer, UserSerializer, ExtraInfoSerializer, MenuSerializer, TableSerializer
from manager_app.models import Reservation, Restaurant, ExtraInfo, Menu, Table
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('users-list', request=request, format=format),
        'reservations': reverse('reservations-list', request=request, format=format)
    })


class ReservationListView(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def get(self, request):
        user = request.user

        if user.is_authenticated:
            restaurants = Restaurant.objects.filter(owner=user)
            restaurants_ids = [res.pk for res in restaurants]
            query_set = Reservation.objects.filter(restaurant__in=restaurants_ids)
        else:
            query_set = Reservation.objects.all()

        serializer = ReservationSerializer(query_set, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReservationDetailsView(generics.GenericAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def get(self, request, res_id):
        query_set = Reservation.objects.get(pk=res_id)
        serializer = ReservationSerializer(query_set)

        return Response(serializer.data)


class TodayReservationsList(generics.GenericAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def get(self, request):
        today = date.today()
        query_set = Reservation.objects.filter(date=today).order_by("hour")
        serializer = ReservationSerializer(query_set, many=True)

        return Response(serializer.data)


class DateReservationsList(generics.GenericAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    def get(self, request, start_date, end_date=None):
        if end_date:
            query_set = Reservation.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date', 'hour')
            pass
        else:
            query_set = Reservation.objects.filter(date=start_date).order_by('hour')

        query_set.order_by("date")
        serializer = ReservationSerializer(query_set, many=True)

        return Response(serializer.data)


class ExtraInfoList(generics.GenericAPIView):
    serializer_class = ExtraInfoSerializer
    queryset = ExtraInfo.objects.all()

    def get(self, request):
        query_set = ExtraInfo.objects.all()
        serializer = ExtraInfoSerializer(query_set, many=True)

        return Response(serializer.data)


class MenuView(generics.GenericAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

    def get(self, request, menu_id=None):
        if menu_id:
            query_set = Menu.objects.get(pk=menu_id)
            serializer = MenuSerializer(query_set)
        else:
            query_set = Menu.objects.all().order_by('-active')
            serializer = MenuSerializer(query_set, many=True)

        return Response(serializer.data)


class TableView(generics.GenericAPIView):
    serializer_class = TableSerializer
    queryset = Table.objects.all()

    def get(self, request, table_id=None):
        if table_id:
            query_set = Table.objects.get(pk=table_id)
            serializer = TableSerializer(query_set)
        else:
            query_set = Table.objects.all()
            serializer = TableSerializer(query_set, many=True)

        return Response(serializer.data)

    def post(self, request, table_id=None):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)