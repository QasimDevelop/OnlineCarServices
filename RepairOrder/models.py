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
    BranchName = models.IntegerField()
    VehicleID = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    Mileage = models.IntegerField(null=True, blank=True)
    MileageUnitName = models.CharField(max_length=100, null=True, blank=True)
    PaymentMethodName = models.CharField(max_length=100, null=True, blank=True)
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
    FuelTankReading = models.FloatField(null=True, blank=True)
    ServiceTypeName = models.CharField(max_length=100, null=True, blank=True)
    SupervisorName = models.CharField(max_length=200, null=True, blank=True)
    IsIRCompleted = models.BooleanField(null=True, blank=True)
    IsMileageVerified = models.BooleanField(null=True, blank=True)
    IsTaxFree = models.BooleanField(null=True, blank=True)
    LaborPrice = models.FloatField(null=True, blank=True)
    DriverName = models.CharField(max_length=500, null=True, blank=True)
    IsWashing = models.BooleanField(null=True, blank=True)
    WashingType = models.CharField(max_length=250, null=True, blank=True)
    IsWarrantyClaim = models.BooleanField(null=True, blank=True)
    VehicleCategoryName = models.CharField(max_length=500, null=True, blank=True)
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

class JobPart(models.Model):
    JobPartID = models.AutoField(primary_key=True)
    JobCard = models.ForeignKey(JobCard,on_delete=models.CASCADE,related_name="parts")
    JobConcern = models.ForeignKey(JobConcern,on_delete=models.SET_NULL,null=True,blank=True,related_name="parts")
    JobCardServiceID = models.IntegerField(null=True, blank=True)
    StockPartID = models.IntegerField(null=True, blank=True)
    IsNew = models.BooleanField(null=True, blank=True)
    PurchasingPrice = models.FloatField(null=True, blank=True)
    SellingPrice = models.FloatField(null=True, blank=True)
    Quantity = models.FloatField(null=True, blank=True)
    RequestedQuantity = models.FloatField(null=True, blank=True)
    TaxAmount = models.FloatField(null=True, blank=True)
    TotalAmount = models.FloatField(null=True, blank=True)
    NetAmount = models.FloatField(null=True, blank=True)
    Notes = models.CharField(max_length=1500, null=True, blank=True)
    JobPartStatusName = models.CharField(max_length=100, null=True, blank=True)
    UnitTypeName = models.CharField(max_length=100, null=True, blank=True)
    JobPartConditionName = models.CharField(max_length=100, null=True, blank=True)
    BrandName = models.CharField(max_length=200, null=True, blank=True)
    JobAlternateID = models.IntegerField(null=True, blank=True)
    PrimaryPartID = models.IntegerField(null=True, blank=True)
    PriorityTypeName = models.CharField(max_length=100, null=True, blank=True)
    AddJobPartTask = models.BooleanField(null=True, blank=True)
    IsInclude = models.BooleanField(null=True, blank=True)
    IsAvailable = models.BooleanField(null=True, blank=True)
    ReadyToDeliverTime = models.DateTimeField(null=True, blank=True)
    ReceivedTime = models.DateTimeField(null=True, blank=True)
    RejectionNote = models.CharField(max_length=2000, null=True, blank=True)
    IsShowOnInvoice = models.BooleanField(null=True, blank=True)
    # Audit fields
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True, related_name='jobparts_created')
    CreatedOn = models.DateTimeField()
    ModifiedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True, related_name='jobparts_modified')
    ModifiedOn = models.DateTimeField(null=True, blank=True)
    IsDeleted = models.BooleanField(default=False)
    class Meta:
        db_table = "JobPart"

    def __str__(self):
        return f"JobPart #{self.JobPartID}"

class JobTask(models.Model):
    JobTaskID = models.AutoField(primary_key=True)
    JobCard = models.ForeignKey(JobCard,on_delete=models.CASCADE,related_name="tasks",db_column="JobCardID")
    JobConcern = models.ForeignKey(JobConcern,on_delete=models.SET_NULL,null=True,blank=True,related_name="tasks",db_column="JobConcernID")
    TaskDescription = models.CharField(max_length=1500, null=True, blank=True)
    JobTaskCategoryName = models.CharField(max_length=100, null=True, blank=True)
    JobTaskTypeName = models.IntegerField(null=True, blank=True)
    Location = models.CharField(max_length=500, null=True, blank=True)
    TotalAmount = models.FloatField(null=True, blank=True)
    QAVerify = models.BooleanField(default=False)
    VerifiedByUser = models.CharField(max_length=300, null=True, blank=True)
    VerifiedOn = models.DateTimeField(null=True, blank=True)
    QAComments = models.CharField(max_length=300, null=True, blank=True)
    QANote = models.CharField(max_length=2000, null=True, blank=True)
    IsInclude = models.BooleanField(null=True, blank=True)
    RepairTypeName = models.CharField(max_length=100, null=True, blank=True)
    LaborTaskID = models.IntegerField(null=True, blank=True)
    LaborTime = models.BooleanField(null=True, blank=True)
    PriorityTypeName = models.CharField(max_length=100, null=True, blank=True)
    IsFree = models.BooleanField(null=True, blank=True)
    TaxAmount = models.FloatField(null=True, blank=True)
    CheckListTypeName = models.CharField(max_length=200, null=True, blank=True)
    LaborHour = models.FloatField(null=True, blank=True)
    LaborMins = models.FloatField(null=True, blank=True)
    IsChargeToCustomer = models.BooleanField(null=True, blank=True)
    LaborDescriptionArabic = models.CharField(max_length=2500, null=True, blank=True)
    IsPendingTaskRemoved = models.BooleanField(null=True, blank=True)
    # Audit fields
    CreatedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True , related_name='jobtasks_created')
    CreatedOn = models.DateTimeField()
    ModifiedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, blank=True , related_name='jobtasks_modified')
    ModifiedOn = models.DateTimeField(null=True, blank=True)
    IsDeleted = models.BooleanField(default=False)
    class Meta:
        db_table = "JobTask"

    def __str__(self):
        return f"JobTask #{self.JobTaskID}"

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
