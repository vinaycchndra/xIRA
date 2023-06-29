from django.shortcuts import render
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
