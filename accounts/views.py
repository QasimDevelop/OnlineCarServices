from django.shortcuts import render
from rest_framework.views import APIView
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
    AppointmentCreateSerializer
)
from .models import ServiceStation # type: ignore
from .models import User, ServiceType,Appointment
from .permissions import IsAdmin, IsServiceStation
from math import radians, sin, cos, sqrt, atan2

# Create your views here.

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
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Appointment.objects.all()  # type: ignore
        elif self.request.user.role == 'stations':
            return Appointment.objects.filter(service_station__owner=self.request.user)  # type: ignore
        else:
            return Appointment.objects.filter(user=self.request.user)  # type: ignore

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Appointment.objects.all()  # type: ignore
        elif self.request.user.role == 'stations':
            return Appointment.objects.filter(service_station__owner=self.request.user)  # type: ignore
        else:
            return Appointment.objects.filter(user=self.request.user)  # type: ignore
