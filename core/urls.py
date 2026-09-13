from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pm/', views.pm_dashboard, name='pm_dashboard'),
    path('crm/', views.crm_dashboard, name='crm_dashboard'),
    path('project/create/', views.create_project, name='create_project'),
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.create_client, name='create_client'),
    path('clients/<int:pk>/edit/', views.edit_client, name='edit_client'),
    path('leads/', views.lead_list, name='lead_list'),
    path('leads/create/', views.create_lead, name='create_lead'),
    path('run-monitoring/', views.run_monitoring, name='run_monitoring'),
]
