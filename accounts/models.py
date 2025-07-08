from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    CHOICES = (
        ("user", "user"),
        ("stations", "stations"),
        ("admin", "admin")
    )
    role = models.CharField(max_length=10, choices=CHOICES, default="user")
    phone = models.CharField(max_length=10, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)

    def __str__(self):
        return self.username

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class ServiceStation(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_stations')
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    services_offered = models.ManyToManyField(ServiceType, related_name='stations')
    is_active = models.BooleanField(default=True)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def set_location(self, lat: float, lng: float) -> None:
        if lat is not None and lng is not None:
            self.latitude = lat
            self.longitude = lng

    def distance_to(self, lat: float, lng: float) -> float:
        """
        Calculate the Haversine distance (in km) between this station and the given lat/lng.
        """
        from math import radians, sin, cos, sqrt, atan2

        if self.latitude is None or self.longitude is None:
            return float('inf')

        R = 6371  # Earth radius in km
        lat1 = radians(float(self.latitude))  # type: ignore
        lon1 = radians(float(self.longitude))  # type: ignore
        lat2 = radians(float(lat))  # type: ignore
        lon2 = radians(float(lng))  # type: ignore
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

class StationService(models.Model):
    station = models.ForeignKey(ServiceStation, on_delete=models.CASCADE, related_name='services')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField()
    is_available = models.BooleanField(default=True)  # type: ignore
    
    class Meta:
        unique_together = ['station', 'service_type']

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service_station = models.ForeignKey(ServiceStation, on_delete=models.CASCADE, related_name='appointments')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        user_str = getattr(self.user, 'username', str(self.user))
        station_str = getattr(self.service_station, 'name', str(self.service_station))
        return f"{user_str} - {station_str} - {self.appointment_date}"
