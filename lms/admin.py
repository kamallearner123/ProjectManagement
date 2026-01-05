from django.contrib import admin
from .models import Mentor, Student, LmsTask

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'expertise', 'user')
    search_fields = ('full_name', 'expertise', 'user__username', 'user__email')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'mentor')
    list_filter = ('mentor',)
    search_fields = ('full_name', 'email', 'phone')

@admin.register(LmsTask)
class LmsTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor', 'scheduled_date', 'due_date', 'status')
    list_filter = ('status', 'mentor')
    search_fields = ('title', 'description', 'feedback')
    filter_horizontal = ('students',)
