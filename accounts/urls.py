from django.urls import path
from .views import HelloView, UserRegistrationView, AdminOnlyView

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
]
