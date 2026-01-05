from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from datetime import datetime
import io
from .models import Invoice
from .forms import InvoiceForm, InvoiceSearchForm

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

@login_required
def invoice_list(request):
    """Display list of invoices with search and filter functionality"""
    search_form = InvoiceSearchForm(request.GET)
    invoices = Invoice.objects.filter(created_by=request.user)
    
    # Apply search filters
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        service_type = search_form.cleaned_data.get('service_type')
        is_paid = search_form.cleaned_data.get('is_paid')
        
        if search:
            invoices = invoices.filter(
                Q(invoice_number__icontains=search) |
                Q(institute_name__icontains=search) |
                Q(institute_gst_number__icontains=search)
            )
        
        if service_type:
            invoices = invoices.filter(service_type=service_type)
        
        if is_paid:
            invoices = invoices.filter(is_paid=is_paid == 'True')
    
    # Calculate statistics
    stats = {
        'total_invoices': invoices.count(),
        'paid_invoices': invoices.filter(is_paid=True).count(),
        'pending_invoices': invoices.filter(is_paid=False).count(),
        'total_revenue': invoices.filter(is_paid=True).aggregate(
            total=Sum('total_amount')
        )['total'] or 0
    }
    
    # Pagination
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'invoices': page_obj,
        'search_form': search_form,
        'stats': stats,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
    }
    
    return render(request, 'invoices/invoice_list.html', context)

@login_required
def invoice_create(request):
    """Create a new invoice"""
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            messages.success(request, f'Invoice {invoice.invoice_number} created successfully!')
            return redirect('invoices:detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
    
    return render(request, 'invoices/invoice_form.html', {'form': form})

@login_required
def invoice_edit(request, pk):
    """Edit an existing invoice"""
    invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, f'Invoice {invoice.invoice_number} updated successfully!')
            return redirect('invoices:detail', pk=invoice.pk)
    else:
        form = InvoiceForm(instance=invoice)
    
    return render(request, 'invoices/invoice_form.html', {'form': form})

@login_required
def invoice_detail(request, pk):
    """Display invoice details"""
    invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})

@login_required
def invoice_delete(request, pk):
    """Delete an invoice"""
    invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        invoice_number = invoice.invoice_number
        invoice.delete()
        messages.success(request, f'Invoice {invoice_number} deleted successfully!')
        return redirect('invoices:list')
    
    return render(request, 'invoices/invoice_confirm_delete.html', {'invoice': invoice})

@login_required
def mark_invoice_paid(request, pk):
    """Mark an invoice as paid"""
    invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        payment_date = request.POST.get('payment_date')
        if payment_date:
            invoice.is_paid = True
            invoice.payment_date = datetime.strptime(payment_date, '%Y-%m-%d').date()
            invoice.save()
            messages.success(request, f'Invoice {invoice.invoice_number} marked as paid!')
        else:
            messages.error(request, 'Please provide a payment date.')
    
    return redirect('invoices:detail', pk=pk)

@login_required
def invoice_pdf(request, pk):
    """Generate PDF for an invoice"""
    invoice = get_object_or_404(Invoice, pk=pk, created_by=request.user)
    
    if not REPORTLAB_AVAILABLE:
        messages.error(request, 'PDF generation is not available. Please install reportlab.')
        return redirect('invoices:detail', pk=pk)
    
    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    
    # Create the PDF object using ReportLab
    buffer = io.BytesIO()
    # Slightly tighter margins for better use of space
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=6,
        textColor=colors.black,
        alignment=2,  # Right alignment
        fontName='Helvetica-Bold'
    )
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        fontName='Helvetica-Bold'
    )
    value_style = ParagraphStyle(
        'Value',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        fontName='Helvetica'
    )
    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
    )
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.whitesmoke,
        fontName='Helvetica-Bold'
    )

    # Helper for currency formatting (avoid special glyphs like ₹)
    def as_currency(amount: float) -> str:
        try:
            return f"INR {amount:,.2f}"
        except Exception:
            return f"INR {amount:.2f}"
    
    # Add header with logo (left) + company details, and right-aligned title
    from django.conf import settings
    import os
    
    # Logo path
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'APT_02.jpg')
    
    # Create header table with left logo and right-aligned title only
    from reportlab.platypus import Image as RLImage

    logo_flowable = None
    if os.path.exists(logo_path):
        try:
            logo_flowable = RLImage(logo_path)
            # Hard limit the size to avoid layout issues
            max_w, max_h = (200, 120)
            logo_flowable._restrictSize(max_w, max_h)
        except Exception:
            logo_flowable = None

    header_table = Table(
        [[logo_flowable if logo_flowable else '', Paragraph("TAX INVOICE", title_style)]],
        colWidths=[2.0*inch, 4.7*inch],
        hAlign='LEFT'
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 8))

    # Company information below the header, full width
    company_title = Paragraph("<b>Apt Computing Labs</b>", label_style)
    address_lines = [
        "12066, Tower 12, Prestige Royale Gardens, Yelahanka",
        "Bangalore, Karnataka - 560064",
        "India",
        "GST: 29BCGPK2447E1ZN",
        "Email: info@aptcomputinglabs.com",
        "Phone: +91 9739858111",
    ]
    company_address = Paragraph("<br/>".join(address_lines), small_style)
    elements.append(company_title)
    elements.append(company_address)
    elements.append(Spacer(1, 12))
    
    # Company information
    # Invoice meta block (right aligned values)
    invoice_info = [
        [Paragraph("Invoice Number:", label_style), Paragraph(invoice.invoice_number, value_style)],
        [Paragraph("Invoice Date:", label_style), Paragraph(invoice.invoice_date.strftime('%B %d, %Y'), value_style)],
        [Paragraph("Due Date:", label_style), Paragraph(invoice.due_date.strftime('%B %d, %Y'), value_style)],
    ]
    invoice_table = Table(invoice_info, colWidths=[1.6*inch, 2.2*inch], hAlign='RIGHT')
    invoice_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(invoice_table)
    elements.append(Spacer(1, 10))
    # Bill To (client info)
    institute_address = (invoice.institute_address or '').replace('\n', '<br/>')
    gst_line = f"GST: {invoice.institute_gst_number}<br/>" if invoice.institute_gst_number else ''
    client_info = Paragraph(
        f"""
        <b>Bill To</b><br/>
        <b>{invoice.institute_name}</b><br/>
        {institute_address}<br/>
        {gst_line}
        """,
        styles['Normal']
    )
    client_block = Table([[client_info]], colWidths=[6.7*inch])
    client_block.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
    ]))
    elements.append(client_block)
    elements.append(Spacer(1, 14))
    
    # Service details table
    service_data = [
        [
            Paragraph('Description', table_header_style),
            Paragraph('Service Type', table_header_style),
            Paragraph('Service Period', table_header_style),
            Paragraph('Amount', table_header_style),
        ]
    ]
    
    # Handle service period - check if dates exist
    if invoice.service_from_date and invoice.service_to_date:
        service_period = Paragraph(
            f"From: {invoice.service_from_date.strftime('%b %d, %Y')}<br/>To: {invoice.service_to_date.strftime('%b %d, %Y')}",
            small_style
        )
    elif invoice.service_from_date and not invoice.service_to_date:
        service_period = Paragraph(
            f"From: {invoice.service_from_date.strftime('%b %d, %Y')}", small_style
        )
    elif invoice.service_to_date and not invoice.service_from_date:
        service_period = Paragraph(
            f"To: {invoice.service_to_date.strftime('%b %d, %Y')}", small_style
        )
    else:
        service_period = Paragraph("Not specified", small_style)
    
    if invoice.service_type == 'training':
        service_data.append([
            Paragraph(invoice.service_description, styles['Normal']),
            Paragraph(
                f"{invoice.get_service_type_display()}<br/>({invoice.training_hours} batches @ INR {invoice.hourly_rate:,.2f}/batch)",
                small_style
            ),
            service_period,
            as_currency(invoice.subtotal),
        ])
    else:
        service_data.append([
            Paragraph(invoice.service_description, styles['Normal']),
            Paragraph(invoice.get_service_type_display(), styles['Normal']),
            service_period,
            as_currency(invoice.subtotal),
        ])
    
    service_table = Table(service_data, colWidths=[3.2*inch, 1.3*inch, 1.4*inch, 0.8*inch])
    service_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a4a4a')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#cccccc')),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#dddddd')),
    ]))
    elements.append(service_table)
    elements.append(Spacer(1, 14))
    
    # Amount calculation
    amount_data = [
        [Paragraph('Subtotal:', label_style), Paragraph(as_currency(invoice.subtotal), value_style)],
        [Paragraph(f'GST ({invoice.gst_percentage}%):', label_style), Paragraph(as_currency(invoice.gst_amount), value_style)],
        [Paragraph('<b>Total Amount:</b>', label_style), Paragraph(f"<b>{as_currency(invoice.total_amount)}</b>", value_style)],
    ]
    
    amount_table = Table(amount_data, colWidths=[1.7*inch, 1.8*inch], hAlign='RIGHT')
    amount_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEABOVE', (0, -1), (-1, -1), 1.2, colors.black),
    ]))
    elements.append(amount_table)
    
    # Payment Details (Bank Info)
    elements.append(Spacer(1, 14))
    bank_title = Paragraph('<b>Payment Details</b>', label_style)
    elements.append(bank_title)
    elements.append(Spacer(1, 6))

    bank_rows = [
        [Paragraph('Bank Name:', label_style), Paragraph('Bank of Baroda', value_style)],
        [Paragraph('Account Holder:', label_style), Paragraph('Apt Computing Labs', value_style)],
        [Paragraph('Account Number:', label_style), Paragraph('74260200002873', value_style)],
        [Paragraph('IFSC Code:', label_style), Paragraph('BARB0VJYELA', value_style)],
        [Paragraph('Branch:', label_style), Paragraph('Yelahanka', value_style)],
    ]
    bank_table = Table(bank_rows, colWidths=[1.6*inch, 4.9*inch])
    bank_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#cccccc')),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#dddddd')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(bank_table)

    # Payment status
    elements.append(Spacer(1, 18))
    status_text = "PAID" if invoice.is_paid else "PENDING"
    status_color = '#2e7d32' if invoice.is_paid else '#c62828'
    status = Paragraph(f"<b>Status:</b> <font color='{status_color}'><b>{status_text}</b></font>", styles['Normal'])
    elements.append(status)

    # Footer note (omit payment reminder if already paid)
    elements.append(Spacer(1, 12))
    if invoice.is_paid:
        footer_note = Paragraph(
            "Thank you for your business.<br/>For any queries, contact us at info@aptcomputinglabs.com.",
            small_style
        )
    else:
        footer_note = Paragraph(
            "Thank you for your business. Please make the payment by the due date.<br/>"
            "For any queries, contact us at info@aptcomputinglabs.com.",
            small_style
        )
    elements.append(footer_note)
    
    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response
