

from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('student/', include("student.urls")),
    path('login/', views.Login, name="login"),
    path('logout/' , views.Logout , name="Logout"),
    path('institute/' , include("institude.urls"))
]
