from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from accounts.models import ProjectManager, Account
from .forms import CreateTicketForm
from django.shortcuts import get_object_or_404
from projects.models import Project
from .models import Task


def manage_ticket(request):
    if request.user.is_project_manager():
        all_task = get_all_tickets_project_manager(request.user)
        all_task = all_task.order_by('-start_date')
        context = {
            'tasks': all_task,
        }
    return render(request, 'manage_ticket.html', context)


def create_ticket(request, project_id=None):
    context = {

    }
    if request.user.is_project_manager():
        if request.method == 'GET':
            print(request.method)
            print(request.user.first_name)
            project_choice, assignee_choice = all_assignees_for_the_project(request.user, project_id)

            if project_choice is None:
                return HttpResponse('You Can Not Create Ticket For this Project')
            form = CreateTicketForm()
            context['form'] = form
            context['project_choice'] = project_choice[0]
            context['assignee_choice'] = assignee_choice

        elif request.method == 'POST':
            print(request.method)
            form = CreateTicketForm(request.POST)
            context['form'] = form
            assignee_id = request.POST['assignee_id']
            if assignee_id == "":
                messages.error(request, "Please Select Assignee Id")
                return render(request, 'tasks.html', context)
            else:
                get_project = get_object_or_404(Project, id=request.POST['project_id'])
                get_assignee = get_object_or_404(Account, id=request.POST['assignee_id'])

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
                messages.success(request, 'Successfully assigned to '+task.assignee.first_name)
                return redirect('manage_ticket')
            else:
                for key, value in form.errors.as_data().items():
                    messages.error(request,  key+": "+str(value[0]))
        return render(request, 'tasks.html', context)
    return HttpResponse("You do not have permission to create Tasks")


def all_assignees_for_the_project(user, project_id):
    project_manager = ProjectManager.objects.get(project_manager__id=user.id)
    projects = project_manager.get_all_project().values_list('id', flat=True)
    if project_id in projects:
        project = Project.objects.get(id=project_id)
        assignee = project.assignees.all()
        project_choice_tuple_list = [(project.id, project)]
        assignee_choice_tuple_list = []
        for ass_choice in assignee:
            assignee_choice_tuple_list.append((ass_choice.id, ass_choice))
        return project_choice_tuple_list, assignee_choice_tuple_list
    return None, None


def get_all_tickets_project_manager(user):
    project_manager = ProjectManager.objects.get(project_manager__id=user.id)
    projects = project_manager.get_all_project()
    if len(projects) >= 1:
        project_1 = projects[0]
        all_tickets = Task.objects.filter(project__id=project_1.id)
        for i in range(1, len(projects)):
            all_tickets = all_tickets.union(Task.objects.filter(project__id=projects[i].id))
        return all_tickets
    return None

