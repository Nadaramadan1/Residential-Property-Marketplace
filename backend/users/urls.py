from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('clientslist/', views.clients_list_page, name='clients_list'),
    path('addClient/', views.add_client_page, name='add_client'),
    path('updateClient/<int:id>/', views.update_client_page, name='update_client'),
    
    path('representativeslist/', views.representatives_list_page, name='representatives_list'),
    path('addRepresentative/', views.add_representative_page, name='add_representative'),
    path('updateRepresentative/<int:id>/', views.update_representative_page, name='update_representative'),

    # APIs
    path('api/clients/', views.list_clients, name='api_clients_list'),
    path('api/clients/<int:id>/', views.get_client, name='api_get_client'),
    path('api/clients/add/', views.add_client_api, name='api_add_client'),
    path('api/clients/update/<int:id>/', views.update_client_api, name='api_update_client'),
    path('api/clients/delete/<int:id>/', views.delete_client_api, name='api_delete_client'),

    path('api/representatives/', views.list_representatives, name='api_reps_list'),
    path('api/representatives/<int:id>/', views.get_representative, name='api_get_rep'),
    path('api/representatives/add/', views.add_representative_api, name='api_add_rep'),
    path('api/representatives/update/<int:id>/', views.update_representative_api, name='api_update_rep'),
    path('api/representatives/delete/<int:id>/', views.delete_representative_api, name='api_delete_rep'),
]