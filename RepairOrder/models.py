from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Vehicle(models.Model):
    VehicleID = models.AutoField(primary_key=True)
    VIN = models.CharField(max_length=100)
    PlateNumber = models.CharField(max_length=50, blank=True, default='')
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles_created', null=True, blank=True)
    CreatedOn = models.DateTimeField(auto_now_add=True)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.PlateNumber

class JobCard(models.Model):
    JobCardID = models.BigAutoField(primary_key=True , auto_created=True)
    JobCardTypeName = models.CharField(max_length=100)
    ServiceStationID = models.ForeignKey('accounts.ServiceStation' , on_delete=models.CASCADE , null=True , blank=True)
    VehicleID = models.ForeignKey('RepairOrder.Vehicle', on_delete=models.CASCADE, null=True, blank=True)
    StatusID = models.IntegerField(null=True, blank=True)
    JobCardStatusName = models.CharField(max_length=100, null=True, blank=True)
    JobCardOpenDate = models.DateTimeField(null=True, blank=True)
    JobCardCloseDate = models.DateTimeField(null=True, blank=True)
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True,related_name='jobcards_created')
    CreatedOn = models.DateTimeField()
    ModifiedOn = models.DateTimeField(null=True, blank=True)
    ModifiedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True,related_name='jobcards_modified')
    IsDeleted = models.BooleanField(default=False)
    JobCardNumber = models.CharField(max_length=50)

    class Meta:
        db_table = "JobCard"

    def __str__(self):
        return self.JobCardNumber

class JobConcern(models.Model):
    JobConcernID = models.AutoField(primary_key=True)
    JobConcernDescription = models.CharField( max_length=2000, null=True,blank=True )
    JobCardID = models.ForeignKey(JobCard, on_delete=models.CASCADE, related_name="concerns")
    JobConcernTypeName = models.CharField(max_length=100,null=True,blank=True)
    IsApproved = models.BooleanField(null=True, blank=True)
    #OldJobConcernID = models.IntegerField(null=True, blank=True)
    NoIssueFound = models.BooleanField(null=True, blank=True)
    IsDeleted = models.BooleanField(default=False)
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True,related_name='jobconcerns_created')
    CreatedOn = models.DateTimeField()
    ModifiedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True,related_name='jobconcerns_modified')
    ModifiedOn = models.DateTimeField(null=True, blank=True)
    IsPendingTaskConcern = models.BooleanField(null=True, blank=True)
    class Meta:
        db_table = "JobConcern"
    def __str__(self):
        return f"JobConcern {self.JobConcernID}"

class ObjectType(models.Model):
    ObjectTypeID = models.AutoField(primary_key=True)
    ObjectTypeNameEnglish= models.CharField()
    TypeNameEnglish = models.CharField()

    def __str__(self):
        return self.ObjectNameEnglish

class ObjectStatus (models.Model):
    
    ObjectStatusID = models.AutoField(primary_key=True)
    ObjectStatusNameEnglish = models.CharField()
    StatusNameEnglish = models.CharField()

    def __str__(self):
        return f'{self.ObjectStatusID , self.ObjectStatusNameEnglish} --> {self.StatusNameEnglish}'
        
class JobCardTechnician (models.Model):
    JobCardTechnicianID = models.AutoField(primary_key=True)
    JobCardID = models.ForeignKey(JobCard , on_delete=models.CASCADE , related_name='assignTechnicians')
    JobCardStatusID = models.IntegerField()
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='jobcardtechnician_created')
    CreatedOn = models.DateTimeField(auto_now=True)
    IsDeleted = models.BooleanField(default=0)

    def __str__(self):
        return f'JobCardTechnician {self.JobCardTechnicianID}'

class TaskTechnician(models.Model):
    TaskTechnicianID = models.AutoField(primary_key=True)
    JobConcernID = models.ForeignKey(JobConcern , on_delete=models.CASCADE , related_name='assignedTechnicians')
    EmployeeID = models.ForeignKey('accounts.Employee' , on_delete=models.CASCADE)
    ActualTimeSpent = models.IntegerField(null=True, blank=True)
    IsAccepted = models.BooleanField(null=True, blank=True)
    AcceptedDateTime = models.DateTimeField(null=True, blank=True)
    EndDateTime = models.DateTimeField(null=True, blank=True)
    IsCompleted = models.BooleanField(default=False)
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='tasktechnician_created')
    CreatedOn = models.DateTimeField(auto_now=True)
    IsDeleted = models.BooleanField(default=0)
    JobCardID = models.ForeignKey('RepairOrder.JobCard', on_delete = models.CASCADE , null=True , blank=True)
    def __str__(self):
        return f'TaskTechnician {self.TaskTechnicianID} - Employee {self.EmployeeID}'