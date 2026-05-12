from django.urls import path
from . import views

urlpatterns = [

    # pages
    path('', views.agreement_page, name='agreement_page'),
    path('add/', views.add_agreement_page, name='add_agreement_page'),
    # APIs
    path('api/list/', views.list_agreements, name='list_agreements'),
    path('api/add/', views.add_agreement, name='add_agreement'),

]