from django.urls import path
from . import views

urlpatterns = [
    # pages
    path('', views.tour_page, name='tour_page'),
    path('add/', views.add_tour_page, name='add_tour_page'),
    # APIs
    path('api/list/', views.list_tours, name='list_tours'),
    path('api/add/', views.add_tour, name='add_tour'),
    path('delete/<int:tour_id>/', views.delete_tour, name='delete_tour'),
]