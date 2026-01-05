from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number', 
        'institute_name', 
        'service_type', 
        'total_amount', 
        'invoice_date',
        'is_paid'
    ]
    list_filter = ['service_type', 'is_paid', 'invoice_date', 'created_at']
    search_fields = ['invoice_number', 'institute_name', 'institute_gst_number']
    readonly_fields = ['invoice_number', 'subtotal', 'gst_amount', 'total_amount', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Invoice Details', {
            'fields': ('invoice_number', 'due_date')
        }),
        ('Client Information', {
            'fields': ('institute_name', 'institute_address', 'institute_gst_number')
        }),
        ('Service Information', {
            'fields': ('service_type', 'service_description', 'service_from_date', 'service_to_date')
        }),
        ('Training Details', {
            'fields': ('training_hours', 'hourly_rate'),
            'classes': ('collapse',),
            'description': 'Fill these fields for training services'
        }),
        ('Software Details', {
            'fields': ('software_amount',),
            'classes': ('collapse',),
            'description': 'Fill this field for software services'
        }),
        ('Financial Details', {
            'fields': ('subtotal', 'gst_percentage', 'gst_amount', 'total_amount')
        }),
        ('Payment Status', {
            'fields': ('is_paid', 'payment_date')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
