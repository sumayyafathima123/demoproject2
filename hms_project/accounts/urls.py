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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from accounts import views


urlpatterns = [


    path('login_view/', views.login_view, name='login_view'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),

 ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
#
