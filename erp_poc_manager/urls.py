from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
    path('logs/', include('logs.urls')),
    path('meetings/', include('meetings.urls')),
    path('invoices/', include('invoices.urls')),
    path('lms/', include('lms.urls')),
    path('api/', include('tasks.api_urls')),
    path('api/', include('logs.api_urls')),
    path('', include('core.urls')),
]
