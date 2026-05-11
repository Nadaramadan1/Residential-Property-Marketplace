"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from . import views

urlpatterns = [
    
    path('admin/', admin.site.urls),
 
    path('users/', include('users.urls')),
<<<<<<< HEAD
    path('reports/', include('reports.urls')),
]
=======
    path('properties/', include('properties.urls')),
      
 
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('agreement/', views.legal_agreement, name='legal_agreement'),
    path('property-details/', views.property_details, name='property_details'),
    path('property-listing/', views.property_listing, name='property_listing'),
    path('property-manager/', views.property_manager, name='property_manager'),
    path('reports/', views.reports, name='reports'),
    path('start/', views.start, name='start'),
    path('tour-scheduling/', views.tour_scheduling, name='tour_scheduling'),
    path('profile/', views.user_rep_profile, name='user_rep_profile'),
] 
>>>>>>> e9792c851276adf8e29650f33abd41a96bfedffa
