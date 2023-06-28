from django import forms
from .models import Project
from django.contrib.admin.widgets import AdminSplitDateTime


class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name', 'project_category', 'project_description', 'estimated_end_date')
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control',  }),
            'project_category': forms.Select(attrs={'class': 'form-control', }),
            'project_description': forms.Textarea(attrs={'class': 'form-control', }),
        }
