from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'due_date', 'institute_name', 'institute_address', 'institute_gst_number',
            'service_type', 'service_description', 'service_from_date', 'service_to_date',
            'training_hours', 'hourly_rate', 'software_amount', 'gst_percentage', 'notes'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'institute_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter institute name'
            }),
            'institute_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter complete address'
            }),
            'institute_gst_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'GST Number (optional)'
            }),
            'service_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'service-type-select'
            }),
            'service_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the service provided'
            }),
            'service_from_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Service start date'
            }),
            'service_to_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Service end date'
            }),
            'training_hours': forms.NumberInput(attrs={
                'class': 'form-control training-field',
                'placeholder': 'Number of training hours',
                'min': '1'
            }),
            'hourly_rate': forms.NumberInput(attrs={
                'class': 'form-control training-field',
                'placeholder': 'Rate per hour',
                'step': '0.01',
                'min': '0.01'
            }),
            'software_amount': forms.NumberInput(attrs={
                'class': 'form-control software-field',
                'placeholder': 'Software license/release amount',
                'step': '0.01',
                'min': '0.01'
            }),
            'gst_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'value': '18.00'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional notes (optional)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default due date to 30 days from today
        if not self.instance.pk:
            self.fields['due_date'].initial = timezone.now().date() + timedelta(days=30)
    
    def clean(self):
        cleaned_data = super().clean()
        service_type = cleaned_data.get('service_type')
        training_hours = cleaned_data.get('training_hours')
        hourly_rate = cleaned_data.get('hourly_rate')
        software_amount = cleaned_data.get('software_amount')
        service_from_date = cleaned_data.get('service_from_date')
        service_to_date = cleaned_data.get('service_to_date')
        
        # Validate service dates
        if service_from_date and service_to_date:
            if service_to_date < service_from_date:
                raise forms.ValidationError(
                    "Service end date cannot be earlier than start date."
                )
        
        # Validation based on service type
        if service_type == 'training':
            if not training_hours or not hourly_rate:
                raise forms.ValidationError(
                    "Training hours and hourly rate are required for training services."
                )
            # Clear software amount for training
            cleaned_data['software_amount'] = None
            
        elif service_type == 'software':
            if not software_amount:
                raise forms.ValidationError(
                    "Software amount is required for software release services."
                )
            # Clear training fields for software
            cleaned_data['training_hours'] = None
            cleaned_data['hourly_rate'] = None
        
        return cleaned_data


class InvoiceSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by invoice number or institute name...'
        })
    )
    service_type = forms.ChoiceField(
        choices=[('', 'All Services')] + Invoice.SERVICE_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    is_paid = forms.ChoiceField(
        choices=[('', 'All'), ('True', 'Paid'), ('False', 'Unpaid')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )