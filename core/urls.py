from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('run-monitoring/', views.run_monitoring, name='run_monitoring'),
]
