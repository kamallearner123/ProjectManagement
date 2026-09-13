from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    path('dashboard/', views.lms_dashboard, name='lms_dashboard'),
    # Mentor
    path('mentors/', views.mentor_list, name='mentor_list'),
    path('mentors/create/', views.mentor_create, name='mentor_create'),
    path('mentors/<int:pk>/edit/', views.mentor_edit, name='mentor_edit'),
    # Student
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    # Tasks
    path('tasks/', views.lms_task_list, name='task_list'),
    path('tasks/create/', views.lms_task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.lms_task_edit, name='task_edit'),
]
