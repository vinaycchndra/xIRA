from django.shortcuts import render, get_object_or_404
from projects.models import Project
from accounts.models import Account



def dashboard(request, user_id=None):
    if user_id is None:
        projects = Project.objects.all()
    else:
        user_object = Account.objects.get(id=user_id)
        projects = user_object.project_set.all()
    context = {
        'projects': projects,
    }
    return render(request, 'landingPage.html', context)


def manager_dashboard(request, manager_id):
    manager_project = Project.objects.filter(project_manager__project_manager__id = manager_id)
    context = {
        'projects': manager_project,
    }
    return render(request, 'landingPage.html', context)

def project_category(request, project_category):
    e