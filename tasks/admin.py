from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'assigned_to', 'project', 'week', 'status', 'duration']
    list_filter = ['status', 'week', 'project', 'assigned_to']
    search_fields = ['title', 'description']
    readonly_fields = ['metrics']
    filter_horizontal = ['dependencies']