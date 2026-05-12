from django.urls import path
from . import views

urlpatterns = [
    # --- صفحات العرض (Page Rendering) ---
    path('', views.view_home, name='home'),
    
    # العملاء (Clients)
    path('clients/', views.clients_list_page, name='clients_list'),
    path('clients/add/', views.add_client_page, name='add_client'),
    path('clients/update/<int:id>/', views.update_client_page, name='update_client'),
    path('clients/delete/<int:id>/', views.delete_client, name='delete_client'),
    
    # المناديب (Representatives)
    path('representatives/', views.representatives_list_page, name='representatives_list'),
    path('representatives/add/', views.add_representative_page, name='add_representative'),
    path('representatives/update/<int:id>/', views.update_representative_page, name='update_representative'),
    path('representatives/delete/<int:id>/', views.delete_representative, name='delete_representative'),
    

    # --- روابط الـ API (JSON) ---
    path('api/clients/', views.list_clients_api, name='list_clients_api'),
    path('api/clients/add/', views.add_client_api, name='add_client_api'),
    path('api/representatives/', views.list_representatives_api, name='list_representatives_api'),
    path('api/representatives/delete/<int:id>/', views.delete_representative_api, name='delete_representative_api'),
]