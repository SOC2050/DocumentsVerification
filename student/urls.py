
from django.urls import path

from . import views

urlpatterns = [

    path('registeration/', views.StudentRegisteration,
         name="StudentRegisteration"),
    path('application/' , views.StudentApplication , name="StudentApplication"),
    path('application/documents/' , views.uploadDocuments , name="UploadDocuments"),
    path('studentbashboard/', views.StudentDashboard, name="StudentDashboard")

]
