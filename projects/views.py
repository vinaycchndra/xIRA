from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import ProjectCreationForm
from .models import Project
from accounts.models import ProjectManager, Account
from django.http import Http404
from django.urls import reverse
from django.db.models import Q
from tickets.models import Task


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
        'search_results': None
    }
    if request.method == 'POST':
        if 'keyword' in request.POST:
            keyword = request.POST['keyword']
            if keyword:
                found_users = Account.objects.filter(
                    Q(first_name__icontains=keyword) |
                    Q(last_name__icontains=keyword) |
                    Q(work_profile__icontains=keyword))
                context['search_results'] = found_users
        else:
            form = ProjectCreationForm(request.POST)
            if form.is_valid():
                project.project_name = form.cleaned_data['project_name']
                project.project_category = form.cleaned_data['project_category']
                project.project_description = form.cleaned_data['project_description']
                project.estimated_end_date = form.cleaned_data['estimated_end_date']
                project.save()
    return render(request, 'edit_project.html', context)


def remove_employee_from_project(request, project_id, user_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.is_project_manager() and project.project_manager.project_manager.id == request.user.id:
        query_set = set(project.assignees.all())
        user = get_object_or_404(Account, id=user_id)
        if user in query_set:
            # Assign all the tickets for that user to the project Manager:
            Task.objects.filter(project__id=project.id, assignee__id=user.id).update(assignee=request.user)
            project.assignees.remove(user)
            project.save()
        url = reverse('edit_project', kwargs={'pk': project_id})
        return redirect(url)
    else:
        return HttpResponse("You can not have permission to remove this person from the project")


def add_employee_to_project(request, project_id, user_id):
    if request.user.is_project_manager():
        project = get_object_or_404(Project, id=project_id)
        query_set = set(project.assignees.all())
        user = get_object_or_404(Account, id=user_id)
        if user not in query_set:
            project.assignees.add(user)
            project.save()
        url = reverse('edit_project', kwargs={'pk': project_id})
        return redirect(url)
    else:
        return HttpResponse("You can not have permission to add this person to the project")



