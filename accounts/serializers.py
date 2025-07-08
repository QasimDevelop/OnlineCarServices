from rest_framework import serializers
from .models import User, ServiceType, ServiceStation, Appointment

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
    
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('user',)

class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('user',)
