from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CreateJobCardView , AllJobCardsView , JobCardAssignDataView , JobCardAssignTechnicianView
urlpatterns = [
    path('create-job-card/',CreateJobCardView.as_view(),name='create-job-card'),
    path('all-job-cards/',AllJobCardsView.as_view(),name='all-job-cards'),
    path('jobcard/<int:jobcard_id>/assign-data/', JobCardAssignDataView.as_view(), name='jobcard-assign-data'),
    path('assignTechnician/', JobCardAssignTechnicianView.as_view(), name='assign-technician')
]
