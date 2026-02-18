from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    HelloView, 
    UserRegistrationView, 
    AdminOnlyView,
    ServiceTypeListCreateView,
    ServiceTypeDetailView,
    ServiceStationListCreateView,
    ServiceStationDetailView,
    NearbyServiceStationsView,
    AppointmentListCreateView,
    AppointmentDetailView,
    StationServiceView,
    AppointmentSlotsByDayView,
)

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
    # Service Types
    path('service-types/', ServiceTypeListCreateView.as_view(), name='service-type-list'),
    path('service-types/<int:pk>/', ServiceTypeDetailView.as_view(), name='service-type-detail'),
    
    # Service Stations
    path('service-stations/', ServiceStationListCreateView.as_view(), name='service-station-list'),
    path('service-stations/<int:pk>/', ServiceStationDetailView.as_view(), name='service-station-detail'),
    path('service-stations/nearby/', NearbyServiceStationsView.as_view(), name='nearby-service-stations'),
    
    # Appointments
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),

    # Get Appointment Slots for a specific day 
    path('appointment-slots/',AppointmentSlotsByDayView.as_view(),name='appointment-slots-by-day'),
    # Get the service types offered by a specific station 
    path('station-services/<int:station_id>/',StationServiceView.as_view(),name='station-services'),
]
