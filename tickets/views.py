from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from accounts.models import ProjectManager, Account, Information
from .forms import CreateTicketForm, DateForm
from django.shortcuts import get_object_or_404
from projects.models import Project
from .models import Task
from .models import status_field, task_type_choices, priority_field
import datetime
from accounts.views import push_notification
from django.core.paginator import Paginator


# Manager Accessible function
def manage_ticket(request):
    url = ""
    count = 0
    for j in request.GET:
        if j != 'page':
            count += 1
    if count > 0:
        url += "?"
    for item in request.GET:
        if item != 'page':
            temp_url = item+"="+request.GET.get(item)+"&"
            url += temp_url
    if url[-1:] == "&":
        url = url[:-1]
    print(url)
    if request.user.is_project_manager():
        project_coice_tuple_list, assignee_choice_tuple_list = get_choice_fields(request.user)
        context = {
            'project_choice': project_coice_tuple_list,
            'assignee_choice': assignee_choice_tuple_list,
            'status_choice': status_field,
            'task_type_choice': task_type_choices,
            'priority_choice': priority_field,
        }
        all_task_query = get_all_tickets_project_manager(request.user)
        query_dic = request.GET

        if 'project_id' in query_dic:
            if query_dic['project_id'] != '' and len(all_task_query) > 0:
                all_task_query = all_task_query.filter(project__id=int(query_dic['project_id']))

        if 'assignee_id' in query_dic:
            if query_dic['assignee_id'] != '' and len(all_task_query) > 0:
                all_task_query = all_task_query.filter(assignee__id=int(query_dic['assignee_id']))

        if 'task_type' in query_dic:
            if query_dic['task_type'] != '' and len(all_task_query) > 0:
                all_task_query = all_task_query.filter(task_type=query_dic['task_type'])

        if 'priority' in query_dic:
            if query_dic['priority'] != '' and len(all_task_query) > 0:
                all_task_query = all_task_query.filter(priority=query_dic['priority'])

        if 'status' in query_dic:
            if query_dic['status'] != '' and len(all_task_query) > 0:
                all_task_query = all_task_query.filter(status=query_dic['status'])

        all_task_query = all_task_query.order_by('-start_date')

        if 'order_by' in query_dic:
            if int(query_dic['order_by']) == 2:
                all_task_query = all_task_query.order_by('start_date')
            if int(query_dic['order_by']) == 3:
                all_task_query = all_task_query.order_by('estimated_end_date')
            if int(query_dic['order_by']) == 4:
                all_task_query = all_task_query.order_by('-estimated_end_date')
        print(request.GET)
        page_no = request.GET.get('page')
        page_object = Paginator(all_task_query, 3)
        if page_no is None:
            all_task_query = page_object.get_page(1)
            print(all_task_query.number)
        else:
            all_task_query = page_object.get_page(page_no)
            print(all_task_query.number)
        context['tasks'] = all_task_query
        context['url'] = url
    return render(request, 'manage_ticket.html', context)


# Manager Accessible function
def create_ticket(request, project_id=None):
    context = {
    }
    if request.user.is_project_manager():
        if request.method == 'GET':
            project_choice, assignee_choice = all_assignees_for_the_project(request.user, project_id)

            if project_choice is None:
                return HttpResponse('You Can Not Create Ticket For this Project')
            form = CreateTicketForm()
            context['form'] = form
            context['project_choice'] = project_choice[0]
            context['assignee_choice'] = assignee_choice

        elif request.method == 'POST':
            form = CreateTicketForm(request.POST)
            context['form'] = form
            assignee_id = request.POST['assignee_id']
            if assignee_id == "":
                messages.error(request, "Please Select Assignee Id")
                return render(request, 'tasks.html', context)
            else:
                get_project = get_object_or_404(Project, id=request.POST['project_id'])
                get_assignee = get_object_or_404(Account, id=request.POST['assignee_id'])
                project_choice, assignee_choice = all_assignees_for_the_project(request.user, get_project.id)
                context['project_choice'] = project_choice[0]
                context['assignee_choice'] = assignee_choice

            if form.is_valid():
                task_type = form.cleaned_data['task_type']
                status = 'Open'
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
                user_message = """A ticket is assigned to you in Project: "{}" """.format(task.project.project_name)
                push_notification(task.assignee, user_message)
                messages.success(request, 'Successfully assigned to '+task.assignee.first_name)
                return redirect('manage_ticket')
            else:
                for key, value in form.errors.as_data().items():
                    messages.error(request,  key+": "+str(value[0]))
        return render(request, 'tasks.html', context)
    return HttpResponse("You do not have permission to create Tasks")


# Manager Accessible function
def edit_ticket(request, ticket_id=None):
    ticket = get_object_or_404(Task, id=ticket_id)
    if request.user.is_project_manager() and ticket.project.project_manager.project_manager.id == request.user.id:
        project_choice, assignee_choice = all_assignees_for_the_project(request.user, ticket.project.id)
        context = {

        }
        date_form = DateForm()
        date_form.fields['date_field'].initial = ticket.estimated_end_date + datetime.timedelta(hours=5, minutes=30)
        context['estimated_date_form'] = date_form
        context['project_choice'] = project_choice[0]
        context['assignee_choice'] = assignee_choice
        context['task'] = ticket
        if request.method == 'GET':
            form = CreateTicketForm(instance=ticket)
            context['form'] = form
            return render(request, 'edit_manager_task.html', context)
        else:
            form = CreateTicketForm(request.POST)
            if form.is_valid():
                ticket.task_type = form.cleaned_data['task_type']
                ticket.status = 'Open'
                ticket.estimated_end_date = form.cleaned_data['estimated_end_date']
                ticket.description = form.cleaned_data['description']
                ticket.short_summary = form.cleaned_data['short_summary']
                ticket.priority = form.cleaned_data['priority']
                assignee_object = Account.objects.get(id=request.POST['assignee_id'])
                ticket.assignee = assignee_object
                ticket.save()
                user_message = """Ticket assigned to you in Project: "{}" is updated""".format(ticket.project.project_name)
                push_notification(ticket.assignee, user_message)
                messages.success(request, 'Successfully updated task')
                return redirect('manage_ticket')
            else:
                context['form'] = form
                for key, value in form.errors.as_data().items():
                    messages.error(request,  key+": "+str(value[0]))
                return render(request, 'edit_manager_task.html', context)


# Manager Accessible function
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Task, id=ticket_id)
    if request.user.is_project_manager() and ticket.project.project_manager.project_manager.id==request.user.id:
        ticket.delete()
        user_message = """Ticket assigned to you in Project: "{}" is deleted""".format(ticket.project.project_name)
        push_notification(ticket.assignee, user_message)
        messages.success(request, 'Ticket deleted successfully')
        return redirect('manage_ticket')
    return HttpResponse("You do not have permission to create Tasks")


# User Accessbile function
def user_manage_ticket(request):
    user_object = Account.objects.get(id=request.user.id)
    projects = user_object.project_set.all()
    project_choice = [(project.id, project.project_name) for project in projects]
    all_task_query = Task.objects.filter(assignee__id=request.user.id)
    context = {
        'project_choice': project_choice,
        'status_choice': status_field,
        'task_type_choice': task_type_choices,
        'priority_choice': priority_field,
    }

    query_dic = request.GET
    if 'project_id' in query_dic:
        if query_dic['project_id'] != '' and len(all_task_query) > 0:
            all_task_query = all_task_query.filter(project__id=int(query_dic['project_id']))

    if 'task_type' in query_dic:
        if query_dic['task_type'] != '' and len(all_task_query) > 0:
            all_task_query = all_task_query.filter(task_type=query_dic['task_type'])

    if 'priority' in query_dic:
        if query_dic['priority'] != '' and len(all_task_query) > 0:
            all_task_query = all_task_query.filter(priority=query_dic['priority'])

    if 'status' in query_dic:
        if query_dic['status'] != '' and len(all_task_query) > 0:
            all_task_query = all_task_query.filter(status=query_dic['status'])

    all_task_query = all_task_query.order_by('-start_date')

    if 'order_by' in query_dic:
        if int(query_dic['order_by']) == 2:
            all_task_query = all_task_query.order_by('start_date')
        if int(query_dic['order_by']) == 3:
            all_task_query = all_task_query.order_by('estimated_end_date')
        if int(query_dic['order_by']) == 4:
            all_task_query = all_task_query.order_by('-estimated_end_date')

    context['tickets'] = all_task_query
    return render(request, 'my_task_dashboard.html', context)


# User Update Ticket view
def update_status(request, ticket_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=ticket_id, assignee__id=request.user.id)
        except Task.DoesNotExist:
            return HttpResponse("Not Found", status=404)
        if request.POST['status'] != '':
            task.status = request.POST['status']
            task.save()
            messages.success(request, "Ticket Status Changes Successfully")
        return redirect('user_ticket_dashboard')

    return HttpResponse('Not Allowed This Way to change the status!!!')


def get_notification(request):
    notify = Information.objects.filter(user__id=request.user.id).order_by('-created_at')
    context = {
        'notification': notify,
    }
    return render(request, 'my_notifications.html', context)


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
            all_tickets = all_tickets | Task.objects.filter(project__id=projects[i].id)
        return all_tickets
    return None


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

