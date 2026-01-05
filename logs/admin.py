from django.contrib import admin
from .models import DailyLog

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'yesterday_summary', 'today_summary']
    list_filter = ['date', 'user']
    search_fields = ['user__username', 'yesterday', 'today']
    readonly_fields = ['date']

    def yesterday_summary(self, obj):
        return obj.yesterday[:50] + '...' if len(obj.yesterday) > 50 else obj.yesterday
    yesterday_summary.short_description = 'Yesterday'

    def today_summary(self, obj):
        return obj.today[:50] + '...' if len(obj.today) > 50 else obj.today
    today_summary.short_description = 'Today'