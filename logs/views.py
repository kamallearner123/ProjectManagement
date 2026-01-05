from django.shortcuts import render, redirect
from .models import DailyLog
from .forms import DailyLogForm

def log_list(request):
    logs = DailyLog.objects.all()
    return render(request, 'logs/log_list.html', {'logs': logs})

def create_log(request):
    if request.method == 'POST':
        form = DailyLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('log_list')
    else:
        form = DailyLogForm()
    return render(request, 'logs/create_log.html', {'form': form})
