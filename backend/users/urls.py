from django.urls import path
from . import views

urlpatterns = [
    path('addClient/', views.add_client, name='add_client'),
    path('clientslist/', views.clients_list, name='clients_list'),
    path('addRepresentative/', views.add_representative, name='add_representative'),
    path('representativeslist/', views.representatives_list, name='representatives_list'),
    path('updateRepresentative/<int:id>/', views.update_representative, name='update_representative'),
    path('updateClient/<int:id>/', views.update_client, name='update_client'),
    path('deleteClient/<int:id>/', views.delete_client, name='delete_client'),
    path('deleteRepresentative/<int:id>/', views.delete_representative, name='delete_representative'),
    path('', views.view_home, name='home'),
]