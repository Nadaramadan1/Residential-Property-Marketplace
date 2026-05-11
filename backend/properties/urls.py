from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_properties),
    path('add/', views.add_property),
    path("update/<int:property_id>/", views.update_property),
    path('delete/<int:property_id>/', views.delete_property),
    path('search/', views.search_properties),
    path("", views.property_page),
    path("add-page/", views.add_property_page, name="add_page"),  
]