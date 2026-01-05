from django import forms
from .models import DailyLog

class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = ['yesterday', 'today', 'blockers', 'comments']
        widgets = {
            'yesterday': forms.Textarea(attrs={'rows': 3}),
            'today': forms.Textarea(attrs={'rows': 3}),
            'blockers': forms.Textarea(attrs={'rows': 2}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
