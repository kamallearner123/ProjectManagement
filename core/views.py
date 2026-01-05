from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import subprocess
import json
import os
from .models import Project
from tasks.models import Task
from logs.models import DailyLog

def home(request):
    projects = Project.objects.all()
    print("Home is called!!!!!")
    
    # Task statistics
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='done').count()
    inprogress_tasks = Task.objects.filter(status='inprogress').count()
    todo_tasks = Task.objects.filter(status='todo').count()
    
    # Recent logs for dashboard
    recent_logs = DailyLog.objects.select_related('user').order_by('-date')[:5]
    
    context = {
        'projects': projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'inprogress_tasks': inprogress_tasks,
        'todo_tasks': todo_tasks,
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
