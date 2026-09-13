from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('dashboard/', views.finance_dashboard, name='finance_dashboard'),
    path('', views.invoice_list, name='list'),
    path('create/', views.invoice_create, name='create'),
    path('upload/', views.client_invoice_upload, name='upload'),
    path('<int:pk>/', views.invoice_detail, name='detail'),
    path('<int:pk>/edit/', views.invoice_edit, name='edit'),
    path('<int:pk>/delete/', views.invoice_delete, name='delete'),
    path('<int:pk>/pdf/', views.invoice_pdf, name='pdf'),
    path('<int:pk>/mark-paid/', views.mark_invoice_paid, name='mark_paid'),
    
    # Financial Management additions
    path('expenses/', views.expense_list, name='expense_list'),
    path('expense/upload/', views.expense_upload, name='expense_upload'),
    path('expense/<int:pk>/edit/', views.expense_edit, name='expense_edit'),
    path('expense/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
]