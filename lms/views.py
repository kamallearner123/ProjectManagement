from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Mentor, Student, LmsTask
from .forms import MentorForm, StudentForm, LmsTaskForm


# Mentors
@login_required
def mentor_list(request):
    mentors = Mentor.objects.all().order_by('full_name')
    return render(request, 'lms/mentor_list.html', {'mentors': mentors})


@login_required
def mentor_create(request):
    if request.method == 'POST':
        form = MentorForm(request.POST)
        if form.is_valid():
            mentor = form.save(commit=False)
            mentor.user = request.user
            mentor.save()
            messages.success(request, 'Mentor created successfully!')
            return redirect('lms:mentor_list')
    else:
        form = MentorForm()
    return render(request, 'lms/mentor_form.html', {'form': form})


@login_required
def mentor_edit(request, pk):
    mentor = get_object_or_404(Mentor, pk=pk)
    if request.method == 'POST':
        form = MentorForm(request.POST, instance=mentor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mentor updated successfully!')
            return redirect('lms:mentor_list')
    else:
        form = MentorForm(instance=mentor)
    return render(request, 'lms/mentor_form.html', {'form': form})


# Students
@login_required
def student_list(request):
    students = Student.objects.select_related('mentor').all().order_by('full_name')
    return render(request, 'lms/student_list.html', {'students': students})


@login_required
def student_create(request):
    # Prefill mentor if provided via query param (?mentor=<id>)
    mentor_id = request.GET.get('mentor') or request.GET.get('mentor_id')
    initial = {}
    if mentor_id:
        try:
            initial['mentor'] = Mentor.objects.get(pk=int(mentor_id))
        except (Mentor.DoesNotExist, ValueError):
            pass

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student created successfully!')
            return redirect('lms:student_list')
    else:
        form = StudentForm(initial=initial)
    return render(request, 'lms/student_form.html', {'form': form})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('lms:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'lms/student_form.html', {'form': form})


# LMS Tasks
@login_required
def lms_task_list(request):
    tasks = LmsTask.objects.select_related('mentor').prefetch_related('students').all().order_by('-created_at')
    return render(request, 'lms/task_list.html', {'tasks': tasks})


@login_required
def lms_task_create(request):
    if request.method == 'POST':
        form = LmsTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('lms:task_list')
    else:
        form = LmsTaskForm()
    return render(request, 'lms/task_form.html', {'form': form})


@login_required
def lms_task_edit(request, pk):
    task = get_object_or_404(LmsTask, pk=pk)
    if request.method == 'POST':
        form = LmsTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('lms:task_list')
    else:
        form = LmsTaskForm(instance=task)
    return render(request, 'lms/task_form.html', {'form': form})
