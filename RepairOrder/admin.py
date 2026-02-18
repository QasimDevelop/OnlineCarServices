from django.contrib import admin
from .models import JobCard , JobConcern, JobPart , ObjectType , ObjectStatus , Vehicle
# Register your models here.

admin.site.register(JobCard)
admin.site.register(JobConcern)
admin.site.register(JobPart)
admin.site.register(ObjectType)
admin.site.register(ObjectStatus)
admin.site.register(Vehicle)