from django.contrib import admin
from .models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['type', 'date_time', 'notes_summary']
    list_filter = ['type', 'date_time']
    search_fields = ['notes']
    
    def notes_summary(self, obj):
        return obj.notes[:50] + '...' if len(obj.notes) > 50 else obj.notes
    notes_summary.short_description = 'Notes'