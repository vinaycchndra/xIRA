from django.shortcuts import render
from .forms import ProjectCreationForm
from .models import Project


def create_project(request):
    form = ProjectCreationForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            project_name = form.cleaned_data['project_name']
            project_category = form.cleaned_data['project_category']
            project_description = form.cleaned_data['project_description']
            estimated_end_date =  form.cleaned_data['estimated_end_date']
            print(project_category, project_name, project_description, estimated_end_date)


    return render(request, 'test.html', context)
