import graphene 
from graphene_django import DjangoObjectType
from .models import Appointment, ServiceStation, ServiceType, User
from django.utils import timezone
from datetime import datetime

class AppointmentType(DjangoObjectType):
    class Meta:
        model = Appointment
        fields = (
            "id", 
            "user", 
            "service_station", 
            "service_type", 
            "appointment_date", 
            "appointment_time",
            "status", 
            "notes",
            "created_at",
            "updated_at"
        )

class ServiceStationType(DjangoObjectType):
    class Meta:
        model = ServiceStation
        fields = ("id", "name", "address", "phone", "email", "is_active","owner")

class ServiceTypeType(DjangoObjectType):
    class Meta:
        model = ServiceType
        fields = ("id", "name", "description", "price")

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role", "phone")

class CreateAppointmentMutation(graphene.Mutation):
    class Arguments:
        appointment_date = graphene.Date(required=True)
        appointment_time = graphene.Time(required=True)
        status = graphene.String(required=True)
        notes = graphene.String()
        service_station = graphene.Int(required=True)
        service_type = graphene.Int(required=True)
        user = graphene.Int(required=True)

    appointment = graphene.Field(AppointmentType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, appointment_date, appointment_time, status, notes, service_station, service_type, user):
        try:
            # Validate status choices
            valid_statuses = [choice[0] for choice in Appointment.STATUS_CHOICES]
            if status not in valid_statuses:
                return CreateAppointmentMutation(
                    success=False,
                    errors=[f"Invalid status. Must be one of: {', '.join(valid_statuses)}"]
                )

            # Check if service station exists
            try:
                station = ServiceStation.objects.get(id=service_station)
            except ServiceStation.DoesNotExist:
                return CreateAppointmentMutation(
                    success=False,
                    errors=["Service station not found"]
                )

            # Check if service type exists
            try:
                service = ServiceType.objects.get(id=service_type)
            except ServiceType.DoesNotExist:
                return CreateAppointmentMutation(
                    success=False,
                    errors=["Service type not found"]
                )

            # Check if user exists
            try:
                user_obj = User.objects.get(id=user)
            except User.DoesNotExist:
                return CreateAppointmentMutation(
                    success=False,
                    errors=["User not found"]
                )

            # Check if appointment date is not in the past
            if appointment_date < timezone.now().date():
                return CreateAppointmentMutation(
                    success=False,
                    errors=["Appointment date cannot be in the past"]
                )

            # Create the appointment
            appointment = Appointment.objects.create(
                user=user_obj,
                service_station=station,
                service_type=service,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status=status,
                notes=notes or ""
            )

            return CreateAppointmentMutation(
                appointment=appointment,
                success=True,
                errors=[]
            )

        except Exception as e:
            return CreateAppointmentMutation(
                success=False,
                errors=[str(e)]
            )

class CreateServiceStationMutation(graphene.Mutation):
    class Arguments:
        name=graphene.String(required=True)
        address=graphene.String(required=True)
        phone=graphene.String(required=True)
        email=graphene.String(required=True)
        is_active=graphene.Boolean(required=True)
        owner=graphene.Int(required=True)

    service_station=graphene.Field(ServiceStationType)
    success=graphene.Boolean()
    errors=graphene.List(graphene.String)
    def mutate(self,info,name,address,phone,email,is_active,owner):
        try:
            try:
                owner_obj=User.objects.get(id=owner)
            except User.DoesNotExist:
                return CreateServiceStationMutation(
                    success=False,
                    errors=["Owner not found"]
                )
            service_station=ServiceStation.objects.create(
                name=name,
                address=address,    
                phone=phone,
                email=email,
                is_active=is_active,
                owner=owner_obj
            )
            return CreateServiceStationMutation(
                service_station=service_station,
                success=True,
                errors=[]
            )
        except Exception as e:
            return CreateServiceStationMutation(
                success=False,
                errors=[str(e)]
            )

class UpdateAppointmentMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        appointment_date = graphene.Date()
        appointment_time = graphene.Time()
        status = graphene.String()
        notes = graphene.String()
        service_station = graphene.Int()
        service_type = graphene.Int()

    appointment = graphene.Field(AppointmentType)
    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, id, **kwargs):
        try:
            # Get the appointment
            try:
                appointment = Appointment.objects.get(id=id)
            except Appointment.DoesNotExist:
                return UpdateAppointmentMutation(
                    success=False,
                    errors=["Appointment not found"]
                )

            # Validate status if provided
            if 'status' in kwargs:
                valid_statuses = [choice[0] for choice in Appointment.STATUS_CHOICES]
                if kwargs['status'] not in valid_statuses:
                    return UpdateAppointmentMutation(
                        success=False,
                        errors=[f"Invalid status. Must be one of: {', '.join(valid_statuses)}"]
                    )

            # Validate service station if provided
            if 'service_station' in kwargs:
                try:
                    station = ServiceStation.objects.get(id=kwargs['service_station'])
                    kwargs['service_station'] = station
                except ServiceStation.DoesNotExist:
                    return UpdateAppointmentMutation(
                        success=False,
                        errors=["Service station not found"]
                    )

            # Validate service type if provided
            if 'service_type' in kwargs:
                try:
                    service = ServiceType.objects.get(id=kwargs['service_type'])
                    kwargs['service_type'] = service
                except ServiceType.DoesNotExist:
                    return UpdateAppointmentMutation(
                        success=False,
                        errors=["Service type not found"]
                    )

            # Update the appointment
            for field, value in kwargs.items():
                setattr(appointment, field, value)
            appointment.save()

            return UpdateAppointmentMutation(
                appointment=appointment,
                success=True,
                errors=[]
            )

        except Exception as e:
            return UpdateAppointmentMutation(
                success=False,
                errors=[str(e)]
            )

class DeleteAppointmentMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    def mutate(self, info, id):
        try:
            appointment = Appointment.objects.get(id=id)
            appointment.delete()
            return DeleteAppointmentMutation(
                success=True,
                errors=[]
            )
        except Appointment.DoesNotExist:
            return DeleteAppointmentMutation(
                success=False,
                errors=["Appointment not found"]
            )
        except Exception as e:
            return DeleteAppointmentMutation(
                success=False,
                errors=[str(e)]
            )

class Query(graphene.ObjectType):
    appointments = graphene.List(AppointmentType)
    appointment = graphene.Field(AppointmentType, id=graphene.Int(required=True))
    user_appointments = graphene.List(AppointmentType, user_id=graphene.Int(required=True))
    station_appointments = graphene.List(AppointmentType, station_id=graphene.Int(required=True))
    service_stations = graphene.List(ServiceStationType)
    service_station=graphene.Field(ServiceStationType,id=graphene.Int(required=True))
    active_service_stations=graphene.List(ServiceStationType)
    def resolve_service_stations(self,info):
        return ServiceStation.objects.all()
    def resolve_active_service_stations(self,info):
        return ServiceStation.objects.filter(is_active=True)
    def resolve_service_station(self,info,id):
        try:
            return ServiceStation.objects.get(id=id)
        except ServiceStation.DoesNotExist:
            return None
    def resolve_appointments(self, info):
        return Appointment.objects.all()

    def resolve_appointment(self, info, id):
        try:
            return Appointment.objects.get(id=id)
        except Appointment.DoesNotExist:
            return None

    def resolve_user_appointments(self, info, user_id):
        return Appointment.objects.filter(user_id=user_id)

    def resolve_station_appointments(self, info, station_id):
        return Appointment.objects.filter(service_station_id=station_id)

class AddServiceType(graphene.Mutation):
    class Arguments:
        name=graphene.String(required=True)
        description=graphene.String(required=True)
        price=graphene.Float(required=True)

    service_type=graphene.Field(ServiceTypeType)
    success=graphene.Boolean()
    errors=graphene.List(graphene.String)
    def mutate(self,info,name,description,price):
        try:
            service_type=ServiceType.objects.create(
                name=name,
                description=description,
                price=price
            )
            return AddServiceType(
                service_type=service_type,
                success=True,
                errors=[]
            )
        except Exception as e:
            return AddServiceType(
                success=False,
                errors=[str(e)]
            )
class UpdateServiceType(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
        name=graphene.String()
        description=graphene.String()
        price=graphene.Float()
    service_type=graphene.Field(ServiceTypeType)
    success=graphene.Boolean()
    errors=graphene.List(graphene.String)
    def mutate(self,info,id,name,description,price):
        try:
            service_type=ServiceType.objects.get(id=id)
            service_type.name=name
            service_type.description=description    
            service_type.price=price
            service_type.save()
            return UpdateServiceType(
                service_type=service_type,
                success=True,
                errors=[]   
            )
        except Exception as e:
            return UpdateServiceType(
                success=False,
                errors=[str(e)]
            )

class Mutation(graphene.ObjectType):
    create_appointment = CreateAppointmentMutation.Field()
    update_appointment = UpdateAppointmentMutation.Field()
    delete_appointment = DeleteAppointmentMutation.Field()
    create_service_station = CreateServiceStationMutation.Field()
    add_service_type = AddServiceType.Field()
    update_service_type = UpdateServiceType.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
