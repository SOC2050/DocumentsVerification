
from django.urls import path, include

from . import views

urlpatterns = [
    path('instituteDashboard/', views.instituteDashboard , name="instituteDashboard"),
    
    
]

