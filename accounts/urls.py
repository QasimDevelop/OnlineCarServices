from django.urls import path
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
    AppointmentDetailView
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
]
