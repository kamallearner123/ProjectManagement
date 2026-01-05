from django.urls import path
from . import views

urlpatterns = [
    path('', views.meeting_list, name='meeting_list'),
    path('create/', views.create_meeting, name='create_meeting'),
]
