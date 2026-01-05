from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_list, name='log_list'),
    path('create/', views.create_log, name='create_log'),
]
