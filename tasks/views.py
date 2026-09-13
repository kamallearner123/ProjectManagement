from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from accounts.decorators import is_employee
from .models import Task, TaskTimeLog, TaskAttachment, Milestone
from .forms import TaskForm
import json

@login_required
@is_employee
def task_list(request):
    """Kanban board view for tasks"""
    tasks = Task.objects.all()
    todo = tasks.filter(status='todo')
    inprogress = tasks.filter(status='inprogress')
    review = tasks.filter(status='review')
    done = tasks.filter(status='done')
    
    return render(request, 'tasks/task_list.html', {
        'todo': todo,
        'inprogress': inprogress,
        'review': review,
        'done': done,
        'all_tasks': tasks
    })

@login_required
@is_employee
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
@is_employee
@require_POST
def update_task_status(request):
    """AJAX endpoint for drag and drop kanban"""
    try:
        data = json.loads(request.body)
        task = get_object_or_404(Task, id=data.get('task_id'))
        task.status = data.get('status')
        task.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@is_employee
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        if 'add_time' in request.POST:
            hours = request.POST.get('hours')
            is_billable = request.POST.get('is_billable') == 'on'
            note = request.POST.get('note')
            if hours:
                TaskTimeLog.objects.create(
                    task=task, user=request.user, hours=hours, 
                    is_billable=is_billable, note=note
                )
        elif 'add_attachment' in request.POST:
            file = request.FILES.get('file')
            if file:
                TaskAttachment.objects.create(
                    task=task, uploaded_by=request.user, file=file
                )
        return redirect('task_detail', pk=pk)
        
    return render(request, 'tasks/task_detail.html', {'task': task})
