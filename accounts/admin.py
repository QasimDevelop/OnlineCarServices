from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(StationService)
admin.site.register(Employee)
admin.site.register(UserRole)
admin.site.register(Roles)
admin.site.register(User)
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

admin.site.register(AppointmentSlots)
