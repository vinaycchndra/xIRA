from django.shortcuts import render
from projects.models import Project


def dashboard(request):
    projects = Project.objects.all()
    context = {
        'projects': projects,
    }
    return render(request, 'landingPage.html', context)
