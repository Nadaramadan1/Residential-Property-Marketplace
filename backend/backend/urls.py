from django.contrib import admin
from django.urls import include, path
from . import views
from users import views as user_views
from reports import views as report_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('dashboard/reports/', include('reports.urls')),
    path('properties/', include('properties.urls')),

    # --- Clients (Delegated to user_views for database access) ---
    path('clients/', user_views.clients_list_page, name='clients_list'),
    path('clients/add/', user_views.add_client_page, name='add_client'),
    path('clients/update/<int:id>/', user_views.update_client_page, name='update_client'),
    path('clients/delete/<int:id>/', user_views.delete_client, name='delete_client'),

    # --- Representatives (Delegated to user_views for database access) ---
    path('representatives/', user_views.representatives_list_page, name='representatives_list'),
    path('representatives/add/', user_views.add_representative_page, name='add_representative'),
    path('representatives/update/<int:id>/', user_views.update_representative_page, name='update_representative'),
    path('representatives/delete/<int:id>/', user_views.delete_representative, name='delete_representative'),
    
    # --- General Pages ---
    path('', views.view_home, name='home'),
    path('dashboard/', report_views.report_dashboard, name='dashboard'),
    path('reports/', report_views.report_dashboard, name='reports'),
]