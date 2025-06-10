"""
URL configuration for hms_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hospital import views

app_name='hospital'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('view_doctor', views.view_doctor, name='view_doctor'),
    path('add_doctor', views.add_doctor, name='add_doctor'),
    path('delete_doctor/<int:id>/', views.delete_doctor, name='delete_doctor'),
    path('view_patient', views.view_patient, name='view_patient'),
    path('delete_patient/<int:id>/', views.delete_patient, name='delete_patient'),
    path('add_patient', views.add_patient, name='add_patient'),
    path('add_appointment', views.add_appointment, name='add_appointment'),
    path('view_appointment', views.view_appointment, name='view_appointment'),
    path('get_doctors_by_speciality/', views.get_doctors_by_speciality, name='get_doctors_by_speciality'),
    path('appointments/<int:id>/', views.delete_appointment, name='delete_appointment'),


    path('appointment_success/', views.appointment_success, name='appointment_success'),




]
