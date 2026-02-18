from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CreateJobCardView , AllJobCardsView
urlpatterns = [
    path('create-job-card/',CreateJobCardView.as_view(),name='create-job-card'),
    path('all-job-cards/',AllJobCardsView.as_view(),name='all-job-cards')
]
