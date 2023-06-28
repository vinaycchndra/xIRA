from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectCreationForm
from .models import Project
from accounts.models import ProjectManager
from django.http import Http404


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
            estimated_end_date = form.cleaned_data['estimated_end_date']
            project = Project.objects.create(project_name=project_name,
                                             project_category=project_category,
                                             project_description=project_description,
                                             estimated_end_date=estimated_end_date,
                                             )
            # Check if project creater is a project manager since manager is also an assignee
            check_if_manager = False
            try:
                manager = ProjectManager.objects.get(project_manager__id=request.user.id)
                project.project_manager = manager
                check_if_manager = True
            except ProjectManager.DoesNotExist:
                pass

            # Always save many to many field after saving the object
            if check_if_manager:
                project.assignees.add(request.user)
            project.save()
            return redirect('dashboard')


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    context = {
        'project': project
    }
    return render(request, 'project_detail.html', context)


def delete_project(request, pk):
    try:
        project = Project.objects.get(id=pk, project_manager__project_manager=request.user)
    except Project.DoesNotExist:
        raise Http404
    project.delete()
    return redirect('dashboard')


def edit_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    form = ProjectCreationForm(instance=project)
    context = {
        'project_form': form,
        'project': project,
    }
    if request.method == 'POST':
        form = ProjectCreationForm(request.POST)
        if form.is_valid():
            project.project_name = form.cleaned_data['project_name']
            project.project_category = form.cleaned_data['project_category']
            project.project_description = form.cleaned_data['project_description']
            project.estimated_end_date = form.cleaned_data['estimated_end_date']
            project.save()
    return render(request, 'edit_project.html', context)