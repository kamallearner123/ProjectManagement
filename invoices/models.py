from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

User = get_user_model()

class Invoice(models.Model):
    SERVICE_TYPES = [
        ('training', 'Training Services'),
        ('software', 'Software Release'),
    ]
    
    # Invoice identification
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    invoice_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    
    # Client details
    institute_name = models.CharField(max_length=200)
    institute_address = models.TextField()
    institute_gst_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Service details
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    service_description = models.TextField()
    
    # Service period
    # Service delivery dates
    service_from_date = models.DateField(null=True, blank=True, help_text="Start date when the service was provided")
    service_to_date = models.DateField(null=True, blank=True, help_text="End date when the service was provided")
    
    # Training specific fields
    training_hours = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        help_text="Required for training services"
    )
    hourly_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Software specific fields
    software_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Tax details
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gst_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=18.00,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Additional details
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(blank=True, null=True)
    
    # Uploaded File (optional replacement for generated PDF)
    pdf_file = models.FileField(upload_to='client_invoices/pdfs/', blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.institute_name}"
    
    def save(self, *args, **kwargs):
        # Generate invoice number if not provided
        if not self.invoice_number:
            self.invoice_number = f"INV-{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate amounts based on service type
        if self.service_type == 'training' and self.training_hours and self.hourly_rate:
            self.subtotal = self.training_hours * self.hourly_rate
        elif self.service_type == 'software' and self.software_amount:
            self.subtotal = self.software_amount
        
        # Calculate GST and total
        self.gst_amount = (self.subtotal * self.gst_percentage) / 100
        self.total_amount = self.subtotal + self.gst_amount
        
        super().save(*args, **kwargs)
    
    @property
    def service_amount(self):
        """Returns the base service amount before tax"""
        if self.service_type == 'training' and self.training_hours and self.hourly_rate:
            return self.training_hours * self.hourly_rate
        elif self.service_type == 'software' and self.software_amount:
            return self.software_amount
        return Decimal('0.00')

class Expense(models.Model):
    vendor_name = models.CharField(max_length=200)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='expenses/pdfs/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.vendor_name} - {self.amount}"

