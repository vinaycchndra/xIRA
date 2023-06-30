from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import ProjectManager, Account
from .forms import CreateTicketForm
from django.shortcuts import get_object_or_404
from projects.models import Project
from .models import Task

def manage_ticket(request, project_id):

    return render(request, 'tasks.html')


def create_ticket(request, ticket_id=None):
    if request.user.is_project_manager:
        project_choice, assignee_choice = get_choice_fields(request.user)
        form = CreateTicketForm()
        context = {
            'form': form,
            'project_choice': project_choice,
            'assignee_choice': assignee_choice,
        }
        if request.method == 'POST':
            form = CreateTicketForm(request.POST)
            get_project = get_object_or_404(Project, id=request.POST['project_id'])
            get_assignee = get_object_or_404(Account, id=request.POST['project_id'])
            if form.is_valid():
                task_type = form.cleaned_data['task_type']
                status = form.cleaned_data['status']
                estimated_end_date = form.cleaned_data['estimated_end_date']
                description = form.cleaned_data['description']
                short_summary = form.cleaned_data['short_summary']
                priority = form.cleaned_data['priority']
                task = Task.objects.create(task_type=task_type,
                                           status=status,
                                           estimated_end_date = estimated_end_date,
                                           description = description,
                                           short_summary = short_summary,
                                           priority=priority,
                                           project=get_project,
                                           assignee=get_assignee,
                                           )
                task.save()
                messages.success(request, 'Successfully create the ticket')
                return redirect('create_ticket')
            else:
                messages.error(request, 'Not valid enteries please fill them back')
                return redirect('create_ticket')
        return render(request, 'tasks.html', context)


def get_choice_fields(user):
    project_manager = ProjectManager.objects.get(project_manager__id=user.id)
    project_choice = project_manager.get_all_project()
    assignee_choice = set()
    for projects in project_choice:
        assignee_choice = assignee_choice.union(set(projects.assignees.all()))
    project_coice_tuple_list = []
    assignee_choice_tuple_list = []

    for pr_choice in project_choice:
        project_coice_tuple_list.append((pr_choice.id, pr_choice))

    for ass_choice in assignee_choice:
        assignee_choice_tuple_list.append((ass_choice.id, ass_choice))

    return project_coice_tuple_list, assignee_choice_tuple_list

