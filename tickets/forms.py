from django import forms
from .models import Task


class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task_type', 'short_summary', 'description', 'status',
                  'priority', 'estimated_end_date')
        widgets = {
            'task_type': forms.Select(attrs={'class': 'form-control', }),
            'status':   forms.Select(attrs={'class': 'form-control', }),
            'priority': forms.Select(attrs={'class': 'form-control', }),
        }


