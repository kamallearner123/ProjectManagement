from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'project', 'week', 'status', 'duration', 'dependencies']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'dependencies': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'dependencies':
                field.widget.attrs['class'] = 'form-control'
