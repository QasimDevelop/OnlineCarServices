from django.contrib import admin

# Register your models here.
from .models import User, ServiceType, ServiceStation, Appointment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('username','email','role')
    list_filter=('role',)
    search_fields=('username','email')
    list_per_page=10
    list_editable=('role',)
    list_display_links=('username','email')
    list_max_show_all=100

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)
    list_filter = ('price',)

@admin.register(ServiceStation)
class ServiceStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'address', 'phone', 'is_active')
    list_filter = ('is_active', 'services_offered')
    search_fields = ('name', 'address', 'owner__username')
    filter_horizontal = ('services_offered',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_station', 'service_type', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date', 'service_type')
    search_fields = ('user__username', 'service_station__name')
    date_hierarchy = 'appointment_date'