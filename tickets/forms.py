from django import forms
from .models import Task
from django.core.exceptions import ValidationError
import datetime


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

    def clean_estimated_end_date(self):
        estimated_end_date = self.cleaned_data["estimated_end_date"]
        estimated_end_date = estimated_end_date - datetime.timedelta(hours=5, minutes=30)
        current_time = datetime.datetime.now().astimezone()
        estimated_end_date_valid = estimated_end_date.astimezone()
        if current_time >= estimated_end_date_valid:
            raise ValidationError("Deadline for the task should be greater than current time!!!")
        return estimated_end_date




