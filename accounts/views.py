from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from django.db.models import Q
from .serializers import (
    UserRegistrationSerializer, 
    ServiceTypeSerializer,
    ServiceStationSerializer,
    ServiceStationCreateSerializer,
    AppointmentSerializer,
    AppointmentCreateSerializer,
    StationServiceSerializer,
    AppointmentSlotsSerializer
)
from .models import AppointmentSlots, ServiceStation # type: ignore
from .models import User, ServiceType,Appointment, StationService
from .permissions import IsAdmin, IsServiceStation
from math import radians, sin, cos, sqrt, atan2

# Create your views here.

class AppointmentSlotsByDayView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AppointmentSlotsSerializer

    def get_queryset(self):
        date_str = self.request.query_params.get("appointment_date")

        if not date_str:
            raise ValidationError({"date": "Date query parameter is required (YYYY-MM-DD)."})

        appointment_date = parse_date(date_str)
        if not appointment_date:
            raise ValidationError({"date": "Invalid date format."})

        day_name = appointment_date.strftime('%A')

        return AppointmentSlots.objects.filter(
            AppointmentDay__iexact=day_name,
            IsDeleted=False,
        ).order_by("AppointmentTime")
class HelloView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}!"})

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()  # type: ignore
    serializer_class = UserRegistrationSerializer
    permission_classes = []  # Allow any user to register

class AdminOnlyView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        return Response({"message": "Hello, Admin!"})

# Service Type Views
class ServiceTypeListCreateView(generics.ListCreateAPIView):
    queryset = ServiceType.objects.all()  # type: ignore
    serializer_class = ServiceTypeSerializer
    permission_classes = [IsAuthenticated]

class ServiceTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceType.objects.all()  # type: ignore
    serializer_class = ServiceTypeSerializer
    permission_classes = [IsAuthenticated]

# Service Station Views
class ServiceStationListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceStationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return ServiceStation.objects.all()  # type: ignore
        elif self.request.user.role == 'stations':
            return ServiceStation.objects.filter(owner=self.request.user)  # type: ignore
        else:
            return ServiceStation.objects.filter(is_active=True)  # type: ignore

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
class StationServiceView(APIView):

    def get(self, request,station_id):
        st = ServiceStation.objects.get(id=station_id)
        services=st.services_offered.all()
        serializer = StationServiceSerializer(services, many=True)
        return Response(serializer.data)
        
class ServiceStationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceStationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return ServiceStation.objects.all()  # type: ignore
        elif self.request.user.role == 'stations':
            return ServiceStation.objects.filter(owner=self.request.user)  # type: ignore
        else:
            return ServiceStation.objects.filter(is_active=True)  # type: ignore

# Nearby Service Stations with Haversine distance
class NearbyServiceStationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = float(request.query_params.get('radius', 10))  # Default 10km

        if not lat or not lng:
            return Response(
                {"error": "Latitude and longitude are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lat = float(lat)
            lng = float(lng)
            stations = ServiceStation.objects.filter( #type: ignore
                is_active=True,
                latitude__isnull=False,
                longitude__isnull=False
            )

            # Calculate distances and filter
            nearby = []
            for station in stations:
                dist = station.distance_to(lat, lng)
                if dist <= radius:
                    nearby.append((dist, station))

            # Sort by distance
            nearby.sort(key=lambda x: x[0])
            result_stations = [station for dist, station in nearby]

            serializer = ServiceStationSerializer(result_stations, many=True)
            return Response(serializer.data)

        except ValueError:
            return Response(
                {"error": "Invalid coordinates"},
                status=status.HTTP_400_BAD_REQUEST
            )

# Appointment Views
class AppointmentListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentSerializer
    
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Appointment.objects.filter(IsDeleted = 0 )  # type: ignore
        elif self.request.user.role == 'stations':
            return Appointment.objects.filter(service_station__owner=self.request.user , IsDeleted = 0 )  # type: ignore
        else:
            return Appointment.objects.filter(user=self.request.user , IsDeleted = 0)  # type: ignore

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Appointment.objects.filter(IsDeleted = 0)  # type: ignore
        elif self.request.user.role == 'stations':
            return Appointment.objects.filter(service_station__owner=self.request.user , IsDeleted = 0)  # type: ignore
        else:
            return Appointment.objects.filter(user=self.request.user , IsDeleted = 0)  # type: ignore
        def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            instance.IsDeleted = True
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)