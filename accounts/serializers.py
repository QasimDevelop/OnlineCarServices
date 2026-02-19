from rest_framework import serializers
from .models import User, ServiceType, ServiceStation, Appointment, StationService
from .models import AppointmentSlots
from django.utils import timezone
from RepairOrder.models import Vehicle
class AppointmentSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentSlots
        fields = (
            "AppointmentSlotsID",
            "AppointmentDay",
            "AppointmentTime",
            "MaxAppointments",
        )

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        return user

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

class ServiceStationSerializer(serializers.ModelSerializer):
    services_offered = ServiceTypeSerializer(many=True, read_only=True)
    latitude = serializers.FloatField(read_only=True)
    longitude = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ServiceStation
        fields = '__all__'
        read_only_fields = ('owner',)

class ServiceStationCreateSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)
    
    class Meta:
        model = ServiceStation
        fields = '__all__'
        read_only_fields = ('owner',)
    
    def create(self, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        
        station = ServiceStation(**validated_data)
        if latitude and longitude:
            station.set_location(latitude, longitude)
        station.save()
        return station
    
    def update(self, instance, validated_data):
        latitude = validated_data.pop('latitude', None)
        longitude = validated_data.pop('longitude', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if latitude and longitude:
            instance.set_location(latitude, longitude)
        
        instance.save()
        return instance

class AppointmentSerializer(serializers.ModelSerializer):
    service_station_name = serializers.CharField(source='service_station.name', read_only=True)
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    plate_number = serializers.CharField(source='VehicleID.PlateNumber', read_only=True)
    vin = serializers.CharField(source='VehicleID.VIN', read_only=True)
    class Meta:
        model = Appointment
        fields = [
            "id",
            "service_station",
            "service_station_name",
            "service_type_name",
            "service_type",
            "notes",
            "plate_number",
            "vin",
            "AppointSlotID",
            "appointment_date",
            "appointment_time",
            "user_name",
            "status"
        ]
        read_only_fields = ('user',)

class AppointmentCreateSerializer(serializers.ModelSerializer):
    plate_number = serializers.CharField(write_only=True)
    vin = serializers.CharField(write_only=True)
    class Meta:
        model = Appointment
        fields = [
            'service_station',
            'service_type',
            'appointment_date',
            'appointment_time',
            'notes',
            'AppointSlotID',
            'plate_number',
            'vin',
        ]
        read_only_fields = ('user',)
    def create(self, validated_data):
        plate_number = validated_data.pop('plate_number')
        user = self.context['request'].user
        vin = validated_data.pop('vin')

        vehicle, created = Vehicle.objects.get_or_create(
            VIN=vin,
            PlateNumber=plate_number,
            CreatedBy=user,
            defaults={'IsActive': True}
        )
        appointment = Appointment.objects.create(
            user=user,
            service_station=validated_data['service_station'],
            service_type=validated_data['service_type'],
            appointment_date=validated_data['appointment_date'],
            appointment_time=validated_data['appointment_time'],
            notes=validated_data.get('notes', ''),
            AppointSlotID=validated_data.get('AppointSlotID', None),
            VehicleID=vehicle
        )
        
        return appointment 

    def validate(self, attrs):
        appointment_date = attrs.get("appointment_date")
        appointment_time = attrs.get("appointment_time")
        service_station = attrs.get("service_station")

        # 1. Date must be today or future
        today = timezone.localdate()
        if appointment_date < today:
            raise serializers.ValidationError(
                {"appointment_date": "Appointment date must be today or a future date."}
            )

        # 2. Get day name from date
        appoint_day = appointment_date.strftime('%A')

        # 3. Check if slot exists
        slot = AppointmentSlots.objects.filter(
            AppointmentDay=appoint_day,
            AppointmentTime=appointment_time,
            IsDeleted=False
        ).first()

        if not slot:
            raise serializers.ValidationError(
                "No appointment slot available for this day and time."
            )

        # 4. Count existing appointments for that date + time
        existing_count = Appointment.objects.filter(
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).count()

        if existing_count >= 3:
            raise serializers.ValidationError(
            "This appointment slot is fully booked. Please select another slot."
        )

    # Optionally, set the slot in attrs for use in create()
        attrs['AppointSlotID'] = slot

        return attrs


class StationServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields= '__all__'