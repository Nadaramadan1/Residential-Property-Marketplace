from django.contrib import admin
from django.urls import include, path
from . import views
from users import views as user_views
from reports import views as report_views
from Tours import views as tours_views
from Agreement import views as agreement_views

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

    #Tour pages
    path('tours/', tours_views.tour_page, name='tour_page'),
    path('tours/add-page/', tours_views.add_tour_page, name='add_tour_page'),
    
    # --- Tours API ---
    path('api/tours/', tours_views.list_tours, name='list_tours_api'),
    path('api/tours/add/', tours_views.add_tour, name='add_tour_api'),
    path('api/tours/update-status/<int:tour_id>/', tours_views.update_tour_status, name='update_tour_status_api'),
    path('api/tours/delete/<int:tour_id>/', tours_views.delete_tour, name='delete_tour_api'),
    
    # Agreement Pages
    path('tours/agreements/', agreement_views.agreement_page, name='agreement_page'),
    path('tours/agreements/add-page/', agreement_views.add_agreement_page, name='add_agreement_page'),
    
    # --- Agreements API ---
    path('api/agreements/', agreement_views.list_agreements, name='list_agreements_api'),
    path('api/agreements/add/', agreement_views.add_agreement, name='add_agreement_api'),
    
    # --- General Pages ---
    path('', views.view_home, name='home'),
    path('dashboard/', report_views.report_dashboard, name='dashboard'),
    path('reports/', report_views.report_dashboard, name='reports'),
]