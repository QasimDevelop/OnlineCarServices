from rest_framework import serializers
from .models import JobCard, JobConcern , Vehicle
from accounts.models import Appointment
from django.utils import timezone

class JobConcernInputSerializer(serializers.Serializer):
    JobConcernDescription = serializers.CharField(max_length=2000)
    JobConcernTypeName = serializers.CharField(max_length=100, required=False, allow_blank=True)

class CreateJobCardSerializer(serializers.ModelSerializer):
    #concerns = JobConcernInputSerializer(many=True, write_only=True)
    appointment_id = serializers.IntegerField(write_only=True, required=False)  # To link the job card to an appointment
    class Meta:
        model = JobCard
        fields = [
            # Add all required JobCard fields here
            'JobCardTypeName',
            'BranchName',
            'JobCardStatusName',
            'CreatedBy',
            'CreatedOn',
            'JobCardNumber',
            'StatusID',
            'appointment_id'
            #'concerns'  # <-- this is the nested input
        ]

    def create(self, validated_data):
        concerns_data = validated_data.pop('concerns', [])
        appointment_id = validated_data.pop('appointment_id', None)
        vehicle = Appointment.objects.get(id=appointment_id).VehicleID 
        jobcard = JobCard.objects.create(**validated_data)
        jobcard.VehicleID = vehicle
        jobcard.save()
        for concern in concerns_data:
            JobConcern.objects.create(
                JobCardID=jobcard,
                JobConcernDescription=concern['JobConcernDescription'],
                JobConcernTypeName=concern.get('JobConcernTypeName', ''),
                CreatedBy=jobcard.CreatedBy,
                CreatedOn=jobcard.CreatedOn,
            )
        # Update appointment status if appointment_id is provided
        if appointment_id:
            try:
                ap = Appointment.objects.get(id=appointment_id)
                ap.status = 'in_progress'
                ap.save()
            except Appointment.DoesNotExist:
                pass  # Optionally, raise a validation error here
        return jobcard
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['VehicleID', 'PlateNumber', 'VIN']

class JobCardListSerializer(serializers.ModelSerializer):
    VehicleID = VehicleSerializer(read_only=True)  # This will include vehicle details in the job card list response
    class Meta:
        model = JobCard
        fields = [
            'JobCardID',
            'JobCardTypeName',
            'BranchName',
            'JobCardStatusName',
            'CreatedBy',
            'CreatedOn',
            'JobCardNumber',
            'StatusID',
            'VehicleID'  
        ]  

