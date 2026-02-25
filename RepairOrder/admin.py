from django.contrib import admin
from .models import JobCard , JobConcern , ObjectType , ObjectStatus , Vehicle , TaskTechnician
# Register your models here.

admin.site.register(JobCard)
admin.site.register(JobConcern)
admin.site.register(ObjectType)
admin.site.register(ObjectStatus)
admin.site.register(Vehicle)
admin.site.register(TaskTechnician)