from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from accounts.decorators import is_pm_or_admin, is_employee
from django.db.models import Sum
from django.utils import timezone
import subprocess
import json
import os
from .models import Project, Client, Lead
from tasks.models import Task
from logs.models import DailyLog
from invoices.models import Invoice
from meetings.models import Meeting
from django.shortcuts import redirect
from django.utils import timezone
from .forms import ProjectForm, ClientForm, LeadForm

@login_required
def home(request):
    projects = Project.objects.all()
    
    # Task statistics
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='done').count()
    inprogress_tasks = Task.objects.filter(status='inprogress').count()
    todo_tasks = Task.objects.filter(status='todo').count()
    open_tasks = inprogress_tasks + todo_tasks
    
    # Financial statistics
    # Ensure we use user-specific invoices if requested, otherwise company-wide.
    # The Invoice model has 'created_by'. Assuming company-wide for dashboard.
    total_revenue = Invoice.objects.filter(is_paid=True).aggregate(total=Sum('total_amount'))['total'] or 0
    outstanding_invoices = Invoice.objects.filter(is_paid=False).count()
    overdue_invoices = Invoice.objects.filter(is_paid=False, due_date__lt=timezone.now().date())
    
    # Meetings
    now = timezone.now()
    upcoming_meetings = Meeting.objects.filter(date_time__gte=now).order_by('date_time')
    upcoming_meetings_count = upcoming_meetings.count()
    
    # Recent activities (using logs + recent tasks)
    recent_logs = DailyLog.objects.select_related('user').order_by('-date')[:5]
    
    context = {
        'projects': projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'inprogress_tasks': inprogress_tasks,
        'todo_tasks': todo_tasks,
        'open_tasks': open_tasks,
        'total_revenue': total_revenue,
        'outstanding_invoices': outstanding_invoices,
        'overdue_invoices': overdue_invoices,
        'upcoming_meetings_count': upcoming_meetings_count,
        'upcoming_meetings': upcoming_meetings[:3],
        'recent_logs': recent_logs,
    }
    
    return render(request, 'core/home.html', context)

@csrf_exempt
@login_required
def run_monitoring(request):
    """Run the Git monitoring script"""
    if request.method == 'POST':
        try:
            # Run the git monitoring script
            script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'git_monitor.py')
            result = subprocess.run(
                ['python', script_path, '--days', '30'], 
                capture_output=True, 
                text=True,
                cwd=os.path.dirname(os.path.dirname(__file__))
            )
            
            if result.returncode == 0:
                # Try to load the results
                try:
                    results_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'git_analysis.json')
                    if os.path.exists(results_path):
                        with open(results_path, 'r') as f:
                            analysis_results = json.load(f)
                        return JsonResponse({
                            'success': True,
                            'results': analysis_results,
                            'output': result.stdout
                        })
                    else:
                        return JsonResponse({
                            'success': True,
                            'output': result.stdout,
                            'message': 'Script completed successfully'
                        })
                except Exception as e:
                    return JsonResponse({
                        'success': True,
                        'output': result.stdout,
                        'note': f'Results file not accessible: {str(e)}'
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'error': result.stderr or 'Script execution failed',
                    'output': result.stdout
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error running monitoring script: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
@is_pm_or_admin
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProjectForm()
    return render(request, 'core/create_project.html', {'form': form})

@login_required
@is_pm_or_admin
def crm_dashboard(request):
    total_clients = Client.objects.count()
    total_leads = Lead.objects.count()
    won_leads = Lead.objects.filter(status='won').count()
    recent_leads = Lead.objects.order_by('-created_at')[:5]
    
    context = {
        'total_clients': total_clients,
        'total_leads': total_leads,
        'won_leads': won_leads,
        'recent_leads': recent_leads,
    }
    return render(request, 'core/crm_dashboard.html', context)

@login_required
@is_employee
def pm_dashboard(request):
    projects = Project.objects.all()
    total_tasks = Task.objects.count()
    open_tasks = Task.objects.exclude(status='done').count()
    recent_logs = DailyLog.objects.order_by('-date')[:5]
    upcoming_meetings = Meeting.objects.filter(date_time__gte=timezone.now()).order_by('date_time')[:5]
    
    context = {
        'projects': projects,
        'total_tasks': total_tasks,
        'open_tasks': open_tasks,
        'recent_logs': recent_logs,
        'upcoming_meetings': upcoming_meetings,
    }
    return render(request, 'core/pm_dashboard.html', context)

@login_required
@is_pm_or_admin
def client_list(request):
    clients = Client.objects.all().order_by('-created_at')
    return render(request, 'core/client_list.html', {'clients': clients})

@login_required
@is_pm_or_admin
def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'core/create_client.html', {'form': form})

@login_required
@is_pm_or_admin
def edit_client(request, pk):
    from django.shortcuts import get_object_or_404
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'core/edit_client.html', {'form': form, 'client': client})

@login_required
@is_pm_or_admin
def lead_list(request):
    leads = Lead.objects.all().order_by('-created_at')
    return render(request, 'core/lead_list.html', {'leads': leads})

@login_required
@is_pm_or_admin
def create_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    else:
        form = LeadForm()
    return render(request, 'core/create_lead.html', {'form': form})
