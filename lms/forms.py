from django import forms
from .models import Mentor, Student, LmsTask


class MentorForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ['full_name', 'expertise', 'bio']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'email', 'phone', 'notes', 'mentor']


class LmsTaskForm(forms.ModelForm):
    class Meta:
        model = LmsTask
        fields = ['title', 'description', 'mentor', 'students', 'scheduled_date', 'due_date', 'status', 'feedback']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
