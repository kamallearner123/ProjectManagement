from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('update-status/', views.update_task_status, name='update_task_status'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
]
